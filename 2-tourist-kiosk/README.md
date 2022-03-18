# Arquitectura Quiosco Turístico

# Acerca de

Esta arquitectura plantea una solución para el procesamiento de datos recolectados por formularios o conversaciones de chat/voz para un quiosco turístico.

La idea es que se las personas puedan interactuar con la plataforma, luego, procesar esta información con el fin de generar mejores experiencias en los centros turísticos.

## Recolectar opiniones en formularios

Con esta arquitectura se podrán integrar datos de formularios **Kobotoolbox** o **Google Docs** desde un API. Cuando se añadan nuevos formularios, estos podrán ser procesados (por ejemplo, para extraer lo más relevante) y luego almacenarlos en un **Storage** para utilizar esa información en algún otro proceso.

Un posible caso de uso luego de tener la información relevante de los formularios almacenada, es mandarlos a una rutina de **procesamiento de lenguaje natural**, esto permitirá analizar la opinión de las personas para averiguar lo que les gusta o disgusta de un lugar, con el fin de identificar puntos de mejora en la experiencia turística.

## Asistencia virtual por chat o voz

Si se desea, se puede integrar **DialogFlow** en conjunto con **Google Assistant** para que las personas puedan interactuar con la aplicación a través de voz. Por ejemplo, un turista puede preguntar al asistente de voz por el nombre de un lugar, actividades, comida, cultura, etc. El asistente le responderá con información del lugar o basándose en las recomendaciones de otros turistas (integrándolo con las opiniones de formularios), incluso, añadiendo un módulo de Traducciones para que el turista pueda preguntar en su idioma nativo.

Alternativamente, se puede integrar el mismo flujo de **DialogFlow** pero esta vez a través de un chat en la aplicación web (un chatbot) que les permita resolver sus preguntas.

# Diagrama

![image info](./tourist-kiosk-architecture.png)

# Costos

Los costos para mantener la arquitectura se pueden obtener utilizando la calculadora de costos de [GCP].

[gcp]: https://cloud.google.com/products/calculator
