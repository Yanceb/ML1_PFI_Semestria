# Horario Inteligente · Proyecto Final Integrador ML1 · Equipo Semestria

Predice en qué **día y jornada** se ofrecerá cada materia el próximo semestre, para **pre-reservar** el horario del estudiante según su patrón actual. Datos reales: programación académica de pregrado presencial de la Universidad EAN, de 2022-2 a 2026-1.

## Contenido
| Archivo | Qué es |
|---|---|
| `informe_PFI.pdf` | Informe técnico (CRISP-DM) |
| `resumen_ejecutivo_EN.pdf` | Resumen ejecutivo en inglés |
| `cuaderno_PFI.ipynb` | Cuaderno reproducible (semilla 2026, rutas relativas) |
| `ficha_datos.md` | Ficha de datos |
| `declaracion_IA.md` | Declaración de uso de IA |
| `anexo_B_datos_reales.md` | Evidencia del bono de datos reales |
| `datos_crudos/` | 8 archivos .xlsx originales |
| `app.py` | Servicio de despliegue (Streamlit) |
| `modelo/` | Modelo guardado y variables para 2026-2 (los genera el cuaderno) |

## Reproducir
```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute cuaderno_PFI.ipynb   # unos 2 minutos; genera modelo/
streamlit run app.py                                          # abre el servicio en http://localhost:8501
```
Versiones usadas: Python 3.13, pandas 3.0, numpy 2.5, scikit-learn 1.9.1, matplotlib 3.11.

## Trazabilidad CRISP-DM
R10 Negocio (informe §1) · R11 Datos (ficha, cuaderno §2) · R12 Preparación (§3) · R13–R14 Modelado (§4) · R13/R17 Evaluación (§5) · R18 Despliegue (§6, `app.py`, resumen EN).
