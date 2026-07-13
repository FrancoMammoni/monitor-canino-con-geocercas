from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage

class VideoWidget(QLabel):
    clicked = pyqtSignal(int, int)         # Clic Izquierdo (Panel)
    right_clicked = pyqtSignal(int, int)   # Clic Derecho (Dibujar Geocerca)
    middle_clicked = pyqtSignal()          # Clic Central (Borrar Geocerca)

    def __init__(self):
        super().__init__()
        # ... (El resto del __init__ queda igual) ...
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Iniciando cámara...")
        self.setStyleSheet("background-color: #121212; color: #FFFFFF; font-size: 14px;")
        self.setMinimumSize(800, 600)
        self._video_w = 1
        self._video_h = 1
        self._current_pixmap = None

    # ... (El método update_frame queda igual) ...
    def update_frame(self, qt_image: QImage):
        self._video_w = qt_image.width()
        self._video_h = qt_image.height()
        self._current_pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = self._current_pixmap.scaled(
            self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        if self._current_pixmap:
            widget_w, widget_h = self.width(), self.height()
            scaled_w, scaled_h = self.pixmap().width(), self.pixmap().height()
            offset_x = (widget_w - scaled_w) / 2
            offset_y = (widget_h - scaled_h) / 2

            # Clic central no requiere mapeo de coordenadas
            if event.button() == Qt.MouseButton.MiddleButton:
                self.middle_clicked.emit()
                super().mousePressEvent(event)
                return

            click_x, click_y = event.pos().x(), event.pos().y()

            if click_x < offset_x or click_x > (offset_x + scaled_w) or \
               click_y < offset_y or click_y > (offset_y + scaled_h):
                if event.button() == Qt.MouseButton.LeftButton:
                    self.clicked.emit(-1, -1)
                return

            real_x = int(((click_x - offset_x) / scaled_w) * self._video_w)
            real_y = int(((click_y - offset_y) / scaled_h) * self._video_h)

            if event.button() == Qt.MouseButton.LeftButton:
                self.clicked.emit(real_x, real_y)
            elif event.button() == Qt.MouseButton.RightButton:
                self.right_clicked.emit(real_x, real_y)
                
        super().mousePressEvent(event)