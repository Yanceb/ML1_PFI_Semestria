# Ficha de datos · Programación académica de pregrado presencial, Universidad EAN (2022-2 a 2026-1)

**Proyecto:** Horario Inteligente · Proyecto Final Integrador, Machine Learning I · Equipo Semestria

## Procedencia
- **Organización de origen:** Universidad EAN (Bogotá, Colombia), Dirección de Registro y Programación Académica.
- **Qué es:** programación académica oficial de pregrado presencial, publicada para los estudiantes al inicio de cada periodo o ciclo: grupos, horarios, días, aulas y docentes.
- **Cómo se obtuvo:** se descargan del portal de estudiantes de la Universidad EAN, página «Gestión de enlace académico-administrativo», sección «PROGRAMACIÓN ACADÉMICA»: https://universidadean.edu.co/estudiantes/gestion-de-enlace-academico-administrativo. Los 8 archivos originales se entregan completos en `datos_crudos/`, con su nombre y versión institucional.
- **Licencia o autorización:** son documentos institucionales publicados para la comunidad estudiantil. No traen licencia abierta explícita y no se cuenta con autorización escrita; se usan solo con fines académicos (ver anexo B).
- **Fecha de acceso para este proyecto:** 22 de octubre de 2026 (los archivos se descargaron en su momento de publicación; la versión de cada archivo va en su nombre, por ejemplo `V7_31012026`).
- **Cita APA 7:** Universidad EAN. (2022–2026). *Programación académica pregrado presencial, periodos 2022-2 a 2026-1* [Conjunto de datos, 8 archivos .xlsx]. Universidad EAN. Consultado el 22 de octubre de 2026, de https://universidadean.edu.co/estudiantes/gestion-de-enlace-academico-administrativo

## Archivos crudos (carpeta `datos_crudos/`)
| Archivo | Periodo | Hojas usadas | Filas útiles |
|---|---|---|---|
| `PROGRAMACION_PREGRADO_PRESENCIAL_2022-2_C4_V1.xlsx` | 2022-2 | FAFCE, FHCS, FIN | 245 |
| `PROGRAMACIoN_PREGRADO-PRESENCIAL_2023-C2-18042023.xlsx` | 2023-1 | FAFCE, FHCS, FIN | 243 |
| `Pregrado-presencial_Planta-fisica-2023-2.xlsx` | 2023-2 | FAFCE, FHCS, FIN | 773 |
| `ProgramacionWebPregradoPresencial2024-1V6.xlsx` | 2024-1 | FAFCE, FHCS, FIN | 1049 |
| `Programacion_Web_Pregrado_Presencial_2024-2_5.xlsx` | 2024-2 | FAFCE, FHCS, FIN | 1049 |
| `Web_Pregrado_Presencial_2025-1_S1-C1 (1).xlsx` | 2025-1 | FAFCE, FHCS, FIN | 1210 |
| `Pregrado_Presencial_2025-2-v1 (2).xlsx` | 2025-2 | FAFCE, FHCS, FIN | 1343 |
| `2026-1_V7_31012026_PREGRADO_PRESENCIAL.xlsx` | 2026-1 | FAFCE, FHCS, FIN | 1243 |

Se excluyen la hoja `COMPLETA` de 2026-1 (duplica las hojas por facultad) y las hojas auxiliares (`Hoja1`, `Hoja6`, `ELECTIVAS`).

## Tabla unificada
- **Filas:** 7155 grupos-horario. **Columnas:** 19. **Materias distintas:** 763.
- **Excluidas a propósito:** nombre del docente y del director (datos personales; 65 % de faltantes en docente), aula y sede (no existen al decidir).

| Columna | Tipo | Faltantes | Distintos | Descripción |
|---|---|---|---|---|
| `periodo` | str | 0.0 % | 8 | Periodo académico (año-semestre), derivado del archivo |
| `facultad` | str | 0.0 % | 3 | Hoja de origen: FIN (Ingeniería), FAFCE (Administración, Finanzas y Ciencias Económicas), FHCS (Humanidades y Ciencias Sociales) |
| `nombre_grupo` | str | 0.1 % | 4922 | Denominación de la unidad de estudio con sufijo de ciclo y grupo (p. ej., C4G1) |
| `codigo_raw` | str | 0.1 % | 3494 | Código de la unidad de estudio o del grupo, como viene en el archivo |
| `hora_ini` | float64 | 0.5 % | 24 | Hora de inicio (decimal) |
| `hora_fin` | float64 | 0.5 % | 48 | Hora de fin (decimal) |
| `creditos` | float64 | 0.1 % | 8 | Créditos académicos |
| `tipologia` | object | 18.8 % | 47 | Tipología (nuclear, transversal, electiva…), sin estandarizar |
| `ciclo` | str | 0.5 % | 6 | C1–C4 (ciclos de 8 semanas) o S1–S2 (semestral) |
| `fecha_ini` | datetime64[us] | 0.5 % | 122 | Fecha de inicio del grupo |
| `fecha_fin` | datetime64[us] | 0.5 % | 129 | Fecha de fin del grupo |
| `LUN` | int64 | 0.0 % | 2 | 1 si el grupo tiene sesión el lunes |
| `MAR` | int64 | 0.0 % | 2 | Ídem martes |
| `MIE` | int64 | 0.0 % | 2 | Ídem miércoles |
| `JUE` | int64 | 0.0 % | 2 | Ídem jueves |
| `VIE` | int64 | 0.0 % | 2 | Ídem viernes |
| `SAB` | int64 | 0.0 % | 2 | Ídem sábado |
| `archivo` | str | 0.0 % | 8 | Archivo crudo de origen |
| `cod_materia` | str | 0.1 % | 763 | Llave de materia: 8 primeros caracteres del código |

## Tabla de modelado (derivada)
21 528 pares (materia, franja, periodo objetivo), con periodos objetivo de 2023-2 a 2026-1, 14 variables numéricas y 3 categóricas, todas calculadas con periodos anteriores al objetivo. La etiqueta `y` vale 1 si la materia abre un grupo en esa franja; la tasa de positivos va de 24 % a 27 %.

## Calidad: hallazgos principales
1. Cobertura desigual: 2022-2 trae solo el ciclo C4, 2023-1 solo el C2, y 2025-1 trae S1 y C1.
2. Deriva de códigos en 2025-2: apenas el 20 % de sus códigos existía en 2025-1.
3. Tipología con 47 variantes de escritura y 18,8 % de faltantes.
4. 49 grupos sin días, 36 sin hora y 16 con hora atípica; se excluyen del conteo de franjas.
5. Sábado con muy poca oferta (cerca del 1 % de los grupos).

## Representatividad
Los datos describen la oferta presencial de pregrado en Bogotá de las tres facultades. No incluyen matrícula, cupos, demanda, cancelaciones posteriores, programas virtuales ni posgrado.
