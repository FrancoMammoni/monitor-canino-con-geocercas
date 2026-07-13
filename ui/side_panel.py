from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class SidePanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedWidth(250)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título
        title = QLabel("Perfil del Sujeto")
        title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 15px;")
        layout.addWidget(title)

        # Datos estructurados fijos
        self.lbl_species = QLabel("<b>Especie:</b> Perro")
        self.lbl_breed = QLabel("<b>Raza:</b> Ovejero Alemán")
        self.lbl_age = QLabel("<b>Edad:</b> 4 años")
        self.lbl_sex = QLabel("<b>Sexo:</b> Macho")
        
        # Estado dinámico
        self.lbl_state = QLabel("<b>Estado Actual:</b> Calculando...")
        self.lbl_state.setStyleSheet("color: #D32F2F; margin-top: 10px;")

        layout.addWidget(self.lbl_species)
        layout.addWidget(self.lbl_breed)
        layout.addWidget(self.lbl_age)
        layout.addWidget(self.lbl_sex)
        layout.addWidget(self.lbl_state)

        self.setLayout(layout)

    def update_state(self, new_state: str):
        self.lbl_state.setText(f"<b>Estado Actual:</b> {new_state}")