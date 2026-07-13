# Monitor canino de estados y geocercas 🐕🤖

Una aplicación nativa de escritorio desarrollada en Python que utiliza visión por computadora e inteligencia artificial (YOLOv8) para monitorizar en tiempo real el comportamiento, postura y ubicación de un perro (específicamente testeado y calibrado para un Ovejero Alemán llamado Toro).

El sistema infiere el estado del perro basándose en la geometría espacial de su detección y permite establecer geocercas interactivas para auditar la invasión de zonas prohibidas.

## 🚀 Funcionalidades Principales (Core Features)

* **Detección en Tiempo Real:** Procesamiento de video en vivo (Webcam/DroidCam/CCTV) utilizando el modelo YOLOv8n.
* **Motor de Estados (Inferencia Postural):** Calcula el nivel de actividad ("Tranquilo" vs "En Alerta") analizando matemáticamente el *Aspect Ratio* de la caja delimitadora del animal.
* **Geocercas Dinámicas (Zonas Prohibidas):** Permite al usuario dibujar polígonos interactivos sobre el feed de video. Si el centro del perro intersecta la zona, el sistema emite una alerta visual de intrusión.
* **Interfaz de Usuario Asíncrona:** UI construida con PyQt6 que opera fluidamente. El procesamiento pesado de OpenCV y YOLO se ejecuta en un `QThread` dedicado, comunicándose mediante señales espaciales mapeadas a la resolución de la interfaz.

## 🛠️ Stack Tecnológico y Arquitectura

* **Frontend:** PyQt6 (Eventos espaciales, Renderizado de interfaz).
* **Backend / Motor de Visión:** OpenCV (cv2) para el análisis geométrico (`pointPolygonTest`, transformaciones afines) y captura de video.
* **Inferencia de IA:** Ultralytics YOLOv8 (Modelo `yolov8n.pt` optimizado para CPU/Real-time).
