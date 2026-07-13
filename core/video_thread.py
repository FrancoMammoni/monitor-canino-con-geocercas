import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage
from ultralytics import YOLO

class VideoThread(QThread):
    frame_ready = pyqtSignal(QImage)
    dog_data_ready = pyqtSignal(str, int, int, int, int)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.model = YOLO('yolov8n.pt')
        # Lista para almacenar los vértices de la geocerca
        self.polygon_points = []

    def set_polygon(self, points):
        """Recibe los vértices dibujados desde la UI"""
        self.polygon_points = points

    def run(self):
        cap = cv2.VideoCapture(0) # Recuerda tu configuración de cámara
        
        while self._run_flag:
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            # 1. Dibujar el polígono (geocerca) siempre, haya o no haya perro
            pts_array = None
            if len(self.polygon_points) > 0:
                pts_array = np.array(self.polygon_points, np.int32).reshape((-1, 1, 2))
                is_closed = len(self.polygon_points) >= 3
                # Dibujamos las líneas en Azul (BGR)
                cv2.polylines(frame, [pts_array], is_closed, (255, 0, 0), 2)
                # Dibujamos puntitos en los vértices
                for p in self.polygon_points:
                    cv2.circle(frame, p, 4, (255, 0, 0), -1)

            results = self.model(frame, classes=[16], verbose=False)
            boxes = results[0].boxes
            
            dog_found = False
            state = "Desconocido"
            x1_f, y1_f, x2_f, y2_f = 0, 0, 0, 0

            for box in boxes:
                dog_found = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w, h = x2 - x1, y2 - y1
                
                # Calcular el Centroide del perro
                cx = x1 + (w // 2)
                cy = y1 + (h // 2)
                
                aspect_ratio = w / h if h > 0 else 1.0

                # --- AUDITORÍA DE GEOCERCA ---
                in_forbidden_zone = False
                if pts_array is not None and len(self.polygon_points) >= 3:
                    # pointPolygonTest devuelve >= 0 si el punto está dentro o en el borde
                    dist = cv2.pointPolygonTest(pts_array, (cx, cy), False)
                    if dist >= 0:
                        in_forbidden_zone = True

                # Lógica de estados con prioridad (La invasión es más importante que la postura)
                if in_forbidden_zone:
                    state = "¡INVASIÓN DE ZONA!"
                    color = (0, 0, 255) # Rojo Fuerte
                elif aspect_ratio > 1.2:
                    state = "Tranquilo"
                    color = (0, 255, 0) # Verde
                else:
                    state = "En Alerta"
                    color = (0, 255, 255) # Amarillo

                x1_f, y1_f, x2_f, y2_f = x1, y1, x2, y2

                # Dibujar Caja
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                # Dibujar Centroide
                cv2.circle(frame, (cx, cy), 5, color, -1)
                
                # Etiqueta
                label = f"Estado: {state}"
                cv2.rectangle(frame, (x1, y1 - 25), (x1 + 250, y1), color, cv2.FILLED)
                # Texto negro si el fondo es amarillo o verde, blanco si es rojo
                txt_color = (0, 0, 0) if not in_forbidden_zone else (255, 255, 255)
                cv2.putText(frame, label, (x1 + 5, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, txt_color, 2)

            # Conversión y emisión
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h_img, w_img, ch = rgb_image.shape
            qt_image = QImage(rgb_image.data, w_img, h_img, ch * w_img, QImage.Format.Format_RGB888)
            
            self.frame_ready.emit(qt_image)
            
            if dog_found:
                self.dog_data_ready.emit(state, x1_f, y1_f, x2_f, y2_f)
            else:
                self.dog_data_ready.emit("No detectado", 0, 0, 0, 0)
            
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()