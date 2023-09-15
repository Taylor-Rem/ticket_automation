from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QInputDialog,
    QLabel,
)
from functools import partial


class BaseWidget(QWidget):
    def _create_button(self, text, callback, layout):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        layout.addWidget(button)

    def create_configured_dropdown(self, items, callback):
        dropdown = QComboBox(self)
        dropdown.addItems(items)
        dropdown.currentIndexChanged.connect(
            lambda index: (
                callback(dropdown.currentText()),
                dropdown.setCurrentIndex(0),
            )
            if index != 0
            else None
        )
        self.layout.addWidget(dropdown)

    def create_text_input(self, title, label, default_text=""):
        text, ok = QInputDialog.getText(self, title, label, text=default_text)
        return text if ok else None
