# Anexo B · Evidencia de datos reales

1. **Hechos observados, no sintéticos.** Son los 8 archivos oficiales de programación académica de pregrado presencial de la Universidad EAN (2022-2 a 2026-1), tal como la universidad los publicó para sus estudiantes. Ninguna fila fue simulada ni generada. Los nombres de archivo conservan la versión institucional, por ejemplo `2026-1_V7_31012026_PREGRADO_PRESENCIAL.xlsx`.
2. **Procedencia verificable.**
   - **Organización:** Universidad EAN, Dirección de Registro y Programación Académica, Bogotá.
   - **Medio:** portal de estudiantes de la Universidad EAN, página «Gestión de enlace académico-administrativo», sección «PROGRAMACIÓN ACADÉMICA»: https://universidadean.edu.co/estudiantes/gestion-de-enlace-academico-administrativo. Desde ahí se descargan los archivos de programación de cada periodo. En la ventana «Programación Académica» aparecen la programación vigente (2026-2) y el apartado «Programación Académica - Anteriores», con los periodos 2026-1, 2025, 2024, 2023 y 2022. Cualquier persona puede verificar y descargar ahí los mismos archivos. Los 8 archivos originales se entregan completos, con el nombre y la versión institucional que traían (por ejemplo, `V7_31012026`).
   - **Fecha de acceso:** 22 de octubre de 2026.
   - **Licencia o autorización:** son documentos institucionales publicados para la comunidad estudiantil. No traen licencia abierta explícita y el equipo no cuenta con una autorización escrita. Se usan solo con fines académicos, sin datos de estudiantes y sin usar los nombres de docentes. El equipo reconoce que esto puede no cumplir por completo el requisito de licencia del bono.
   - **Cita APA 7:** Universidad EAN. (2022–2026). *Programación académica pregrado presencial, periodos 2022-2 a 2026-1* [Conjunto de datos]. Universidad EAN. Consultado el 22 de octubre de 2026, de https://universidadean.edu.co/estudiantes/gestion-de-enlace-academico-administrativo
3. **Archivo crudo:** va completo en `datos_crudos/` (8 archivos .xlsx, unos 20 MB).
4. **Datos de personas y tratamiento ético.** Los archivos traen nombres de docentes y directores de unidad de estudio. Son información institucional pública, pero son datos personales según la Ley 1581 de 2012 de Colombia (protección de datos personales) y el Decreto 1377 de 2013. El tratamiento fue el siguiente:
   - No se usan como variables.
   - No aparecen en la tabla de modelado, en las salidas ni en la app.
   - Se conserva solo un indicador agregado: si el grupo tiene docente asignado.
   - No hay datos de estudiantes.
5. **Tamaño y suciedad real.** Hay 7 155 filas de grupo-horario y 21 528 filas de modelado. El diagnóstico (informe §2 y `ficha_datos.md`) muestra la suciedad real que se encontró:
   - Encabezados en filas distintas.
   - Nombres de columna y formatos de hora y día heterogéneos.
   - Cobertura parcial en algunos periodos.
   - Deriva de códigos.
   - Tipología con 47 variantes.
   - Grupos sin día ni hora.
   - Nombres truncados.
6. **No es un conjunto de los cuadernos de la unidad ni un conjunto clásico de tutorial.**
