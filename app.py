"""Horario Inteligente · servicio de despliegue (Streamlit).
Uso:  pip install -r requirements.txt  &&  streamlit run app.py
Carga el modelo final guardado por el cuaderno (modelo/modelo_horario_operacion.joblib) y las variables
de 2026-2 construidas solo con historia hasta 2026-1 (modelo/variables_2026-2.csv)."""
import joblib, pandas as pd, streamlit as st

DIAS = ['LUN', 'MAR', 'MIE', 'JUE', 'VIE', 'SAB']
JORNADAS = {'MAN': 'Mañana (antes de 12:00)', 'TAR': 'Tarde (12:00–17:59)', 'NOC': 'Noche (18:00 o después)'}

@st.cache_resource
def cargar():
    paquete = joblib.load('modelo/modelo_horario_operacion.joblib')
    X = pd.read_csv('modelo/variables_2026-2.csv')
    X['p'] = paquete['modelo'].predict_proba(X[paquete['X_COLS']])[:, 1]
    return paquete, X

paquete, X = cargar()
U = paquete['umbral']
st.title('Horario Inteligente · pre-reserva para 2026-2')
st.caption(f'Modelo: regresión logística · umbral de reserva {U:.2f} (costo FP:FN = 2:1). El modelo sugiere; usted confirma.')

st.subheader('1. ¿En qué franjas estudia hoy?')
franjas = []
cols = st.columns(len(DIAS))
for c, d in zip(cols, DIAS):
    with c:
        st.markdown(f'**{d}**')
        for j in JORNADAS:
            if st.checkbox(j, key=d + j, help=JORNADAS[j]):
                franjas.append(f'{d}_{j}')

st.subheader('2. ¿Qué materias le faltan?')
catalogo = X.drop_duplicates('cod_materia').assign(etq=lambda d: d.cod_materia + ' · ' + d.materia.fillna(''))
elegidas = st.multiselect('Materias pendientes', catalogo.etq.sort_values().tolist())
codigos = [e.split(' · ')[0] for e in elegidas]

if st.button('Proponer horario') and codigos:
    usadas, filas = set(), []
    for m in codigos:
        c = X[X.cod_materia == m].sort_values('p', ascending=False)
        pref = c[c.franja.isin(franjas) & ~c.franja.isin(usadas)]
        if len(pref) and pref.iloc[0].p >= U and not pref.iloc[0].franja.startswith('SAB'):
            r = pref.iloc[0]; usadas.add(r.franja)
            filas.append({'Materia': r.materia, 'Franja': r.franja, 'Probabilidad': round(r.p, 2), 'Acción': '✅ PRE-RESERVAR'})
        else:
            alt = c[~c.franja.isin(usadas)].head(1)
            filas.append({'Materia': c.materia.iloc[0], 'Franja': alt.franja.iloc[0], 'Probabilidad': round(alt.p.iloc[0], 2),
                          'Acción': '⚠️ Revisar a mano (fuera de su patrón, sábado o poco segura)'})
    st.dataframe(pd.DataFrame(filas), use_container_width=True)
    st.info('Sábados y materias con código nuevo siempre se revisan a mano: el modelo no tiene evidencia suficiente para reservarlos.')

with st.expander('Cómo se vigila y cuándo se reentrena'):
    st.write('Al publicarse la programación oficial se mide la precisión real de las reservas por jornada y facultad. '
             'Se reentrena cada semestre; se alerta si la precisión cae por debajo de 0,80 o si más del 30 % de las materias no tiene historia.')
