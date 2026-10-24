"""Lógica de pre-reserva de Horario Inteligente, separada de la interfaz para poder probarla.
La usan app.py (servicio Streamlit) y la misma regla aparece en recomendar() del cuaderno."""
from pathlib import Path
import joblib
import pandas as pd

BASE = Path(__file__).resolve().parent
RUTA_MODELO = BASE / 'modelo' / 'modelo_horario_operacion.joblib'
RUTA_VARIABLES = BASE / 'modelo' / 'variables_2026-2.csv'


def cargar(ruta_modelo=RUTA_MODELO, ruta_variables=RUTA_VARIABLES):
    """Carga el modelo guardado por el cuaderno y calcula la probabilidad de cada par (materia, franja) de 2026-2."""
    paquete = joblib.load(ruta_modelo)
    X = pd.read_csv(ruta_variables)
    X['p'] = paquete['modelo'].predict_proba(X[paquete['X_COLS']])[:, 1]
    X['materia'] = X['materia'].fillna(X['cod_materia'])          # sin nombre: se muestra el código
    return paquete, X


def proponer(X, franjas_estudiante, materias, umbral):
    """Recorre las materias en el orden recibido. Pre-reserva la franja del patrón del estudiante con mayor
    probabilidad si supera el umbral, no es sábado y no choca con otra ya reservada. Si no, sugiere la mejor
    franja libre para revisar a mano."""
    perfil = set(franjas_estudiante)
    usadas, filas = set(), []
    for m in materias:
        c = X[X.cod_materia == m].sort_values('p', ascending=False)
        if c.empty:   # materia sin historia (código nuevo): no está en las predicciones
            filas.append({'Materia': m, 'Franja': '-', 'Probabilidad': None,
                          'Acción': 'Revisar a mano: materia sin historia (código nuevo)'})
            continue
        # los sábados se quitan ANTES de elegir: un sábado nunca bloquea otra franja válida del patrón
        pref = c[c.franja.isin(perfil) & ~c.franja.isin(usadas) & ~c.franja.str.startswith('SAB')]
        if len(pref) and pref.iloc[0].p >= umbral:
            r = pref.iloc[0]
            usadas.add(r.franja)
            filas.append({'Materia': r.materia, 'Franja': r.franja, 'Probabilidad': round(float(r.p), 2),
                          'Acción': 'PRE-RESERVAR'})
            continue
        alt = c[~c.franja.isin(usadas)].head(1)
        if alt.empty:
            filas.append({'Materia': c.materia.iloc[0], 'Franja': '-', 'Probabilidad': None,
                          'Acción': 'Revisar a mano: todas sus franjas ya están ocupadas'})
        else:
            motivo = 'fuera de su patrón' if not (c.franja.isin(perfil) & ~c.franja.str.startswith('SAB')).any() \
                else 'probabilidad bajo el umbral o franja ocupada'
            filas.append({'Materia': c.materia.iloc[0], 'Franja': alt.franja.iloc[0],
                          'Probabilidad': round(float(alt.p.iloc[0]), 2),
                          'Acción': f'Sugerencia, revisar a mano ({motivo})'})
    return pd.DataFrame(filas)
