# Declaración de uso de inteligencia artificial

**Equipo Semestria** · Proyecto Final Integrador, Machine Learning I

## Herramienta
Claude (Anthropic), modelo Claude Opus 5.5, en la aplicación web de claude.ai con ejecución de código. La usaron las dos integrantes: **Bresleny Yanira Benavides Cabiche** y **Paula Andrea Bustos**.

## Prompt o instrucción central
«Con las instrucciones del Proyecto Final y los 8 archivos de programación académica de pregrado presencial de la EAN, desarrolla el proyecto con esta idea: una IA que, con base en tu horario, te reserve de una vez el horario del siguiente semestre. Es decir, si siempre tienes clase los sábados, buscará las materias del sábado y te las pondrá.» Antes se usaron otros prompts en la misma herramienta para resumir los materiales del curso.

## Qué aceptamos y por qué
- La **formulación** como clasificación binaria por par (materia, franja), porque convierte la idea en una pregunta con etiqueta observable.
- La **unificación** de los 8 archivos con detección automática de encabezados. La revisamos contra los archivos originales: filas por periodo y días marcados.
- La **partición temporal** con validación hacia adelante y la prueba 2026-1 consultada una sola vez.
- **Excluir** docente, aula y fechas del periodo objetivo por fuga y por ética.
- Elegir la **regresión logística** por el criterio de una desviación estándar, declarado antes de ver la prueba.
- Reportar con honestidad que en 2026-1 la regla de persistencia tuvo menor costo que el modelo.

## Qué descartamos o corregimos
- **Re-ponderar clases (`class_weight='balanced'`):** la primera versión lo usaba y producía probabilidades infladas (umbral óptimo de 0,95). Lo quitamos porque la app muestra probabilidades al estudiante.
- **Razón de costo 3:1:** con esa razón el modelo casi nunca reservaba. La cambiamos a 2:1, con la justificación de que los cupos de las franjas apetecidas se agotan, y dejamos la sensibilidad a 1:1, 3:1 y 5:1 en el informe.
- **Población inicial:** al principio se evaluaban materias que desaparecían por el cambio de códigos de 2025-2, lo que volvía falsos positivos a todas sus franjas. Redefinimos la población a las materias que abren en el periodo objetivo y lo declaramos como supuesto.
- **Fuga de disponibilidad detectada en la revisión final:** la facultad y los créditos de cada materia se tomaban de todos los periodos, incluida la prueba. Se corrigió para usar solo periodos anteriores al objetivo; las cifras cambiaron en el tercer decimal.
- **El recomendador del cuaderno reservaba sábados** aunque el informe dice que van siempre a revisión manual. Se corrigió para que coincida con la app.

## Qué podemos defender sin la herramienta
- **Partición temporal y no aleatoria:** la herramienta predice un semestre futuro, así que entrenamos con el pasado y evaluamos en el siguiente. Una partición aleatoria habría usado el futuro para predecir el pasado y habría inflado los resultados.
- **Columnas excluidas:** docente, aula, fechas y número de grupos del periodo objetivo, porque no existen el día de decidir (fuga de disponibilidad). Los nombres de personas se excluyeron también por protección de datos.
- **Precisión promedio en lugar de exactitud:** solo 1 de cada 4 pares se abre. Un modelo que dijera siempre «no» tendría 75 % de exactitud sin servir para nada; la precisión promedio mide qué tan bien encuentra las franjas que sí abren.
- **Umbral de 0,71:** es el que minimiza el costo en validación cuando un falso positivo cuesta el doble que un falso negativo. Se fijó antes de mirar la prueba y no se cambió después.
- **Por qué recomendamos un piloto aunque la persistencia ganó en costo en 2026-1:** el modelo ordena mejor y sus reservas son más confiables (90 % de precisión), pero ese semestre el umbral resultó conservador; por eso proponemos recalibrarlo cada semestre y que el estudiante confirme las reservas.
- **Por qué el sábado nunca se reserva:** casi no hay oferta presencial de pregrado los sábados (cerca del 1 % de los grupos), así que no hay evidencia suficiente para prometer una reserva.
- **Modelo elegido:** la regresión logística quedó a menos de una desviación estándar del mejor modelo y es la más simple, con la menor brecha entre entrenamiento y validación.
