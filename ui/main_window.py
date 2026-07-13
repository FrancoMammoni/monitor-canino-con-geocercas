from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from ui.video_widget import VideoWidget
from ui.side_panel import SidePanel
from core.video_thread import VideoThread

class MainWindow(QMainWindow):
    def __init__(self):
        # ... (inicialización previa de la ventana, igual que antes) ...
        super().__init__()
        self.setWindowTitle("Monitor de Excitación Canina")
        self.resize(1100, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.video_canvas = VideoWidget()
        self.side_panel = SidePanel()
        self.side_panel.hide()

        main_layout.addWidget(self.video_canvas, stretch=1)
        main_layout.addWidget(self.side_panel)

        # Variables de estado
        self.dog_x1, self.dog_y1, self.dog_x2, self.dog_y2 = 0, 0, 0, 0
        self.geofence_points = [] # <-- Nueva lista para la geocerca

        # Conectar señales del mouse
        self.video_canvas.clicked.connect(self._handle_left_click)
        self.video_canvas.right_clicked.connect(self._add_geofence_point) # <-- Nueva conexión
        self.video_canvas.middle_clicked.connect(self._clear_geofence)   # <-- Nueva conexión

        self.vision_thread = VideoThread()
        self.vision_thread.frame_ready.connect(self.video_canvas.update_frame)
        self.vision_thread.dog_data_ready.connect(self._update_dog_data)
        self.vision_thread.start()

    def _update_dog_data(self, state: str, x1: int, y1: int, x2: int, y2: int):
        self.dog_x1, self.dog_y1, self.dog_x2, self.dog_y2 = x1, y1, x2, y2
        if not self.side_panel.isHidden():
            self.side_panel.update_state(state)

    def _handle_left_click(self, x: int, y: int):
        if (self.dog_x1 <= x <= self.dog_x2) and (self.dog_y1 <= y <= self.dog_y2):
            self.side_panel.show()
        else:
            self.side_panel.hide()

    # --- NUEVOS MÉTODOS DE GEOCERCA ---
    def _add_geofence_point(self, x: int, y: int):
        if x < 0 or y < 0:
            return
        self.geofence_points.append((x, y))
        # Actualizamos el hilo en tiempo real
        self.vision_thread.set_polygon(self.geofence_points)

    def _clear_geofence(self):
        self.geofence_points.clear()
        self.vision_thread.set_polygon(self.geofence_points)

    def closeEvent(self, event):
        self.vision_thread.stop()
        event.accept()