"""Horario Inteligente · servicio de despliegue (Streamlit).
Uso:  pip install -r requirements.txt  &&  streamlit run app.py
Carga el modelo final guardado por el cuaderno (modelo/modelo_horario_operacion.joblib) y las variables
de 2026-2 construidas solo con historia hasta 2026-1 (modelo/variables_2026-2.csv)."""
import pandas as pd
import streamlit as st

from recomendador import cargar, proponer

DIAS = ['LUN', 'MAR', 'MIE', 'JUE', 'VIE', 'SAB']
JORNADAS = {'MAN': 'Mañana (antes de 12:00)', 'TAR': 'Tarde (12:00–17:59)', 'NOC': 'Noche (18:00 o después)'}


@st.cache_resource
def cargar_cache():
    return cargar()


paquete, X = cargar_cache()
U = paquete['umbral']
nombre_modelo = paquete.get('nombre', 'modelo final del cuaderno')

st.title('Horario Inteligente · pre-reserva para 2026-2')
st.caption(f'Modelo: {nombre_modelo} · umbral de reserva {U:.2f} (costo FP:FN = 2:1). El modelo sugiere; usted confirma.')

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
st.caption('Elíjalas en orden de prioridad: las primeras se quedan con las mejores franjas. '
           'Solo aparecen materias con historia; las de código nuevo se gestionan a mano.')
catalogo = X.drop_duplicates('cod_materia').assign(etq=lambda d: d.cod_materia + ' · ' + d.materia.astype(str))
elegidas = st.multiselect('Materias pendientes', catalogo.etq.sort_values().tolist())
codigos = [e.split(' · ')[0] for e in elegidas]

if st.button('Proponer horario'):
    if not franjas:
        st.warning('Marque al menos una franja en la que estudia hoy.')
    elif not codigos:
        st.warning('Elija al menos una materia pendiente.')
    else:
        st.dataframe(proponer(X, franjas, codigos, U), width='stretch', hide_index=True)
        st.info('Los sábados nunca se pre-reservan: casi no hay oferta presencial y el modelo no tiene evidencia suficiente.')

with st.expander('Cómo se vigila y cuándo se reentrena'):
    st.write('Al publicarse la programación oficial se mide la precisión real de las reservas por jornada y facultad. '
             'Se reentrena cada semestre; se alerta si la precisión cae por debajo de 0,80 o si más del 30 % de las materias no tiene historia.')
