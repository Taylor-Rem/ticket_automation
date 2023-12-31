from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QLineEdit,
    QLabel,
)
from functools import partial


class BaseWidget(QWidget):
    def _create_button(self, text, callback, layout):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        layout.addWidget(button)
        return button

    def create_configured_dropdown(self, items, callback=None):
        dropdown = QComboBox(self)
        dropdown.addItems(items)
        if callback:
            dropdown.currentIndexChanged.connect(
                lambda index: (
                    callback(dropdown.currentText()),
                    dropdown.setCurrentIndex(0),
                )
                if index != 0
                else None
            )
        self.layout.addWidget(dropdown)
        return dropdown

    def create_text_input(self, default_text="", label=None):
        if label:
            label = QLabel(label)
            self.layout.addWidget(label)
        text_input = QLineEdit(self)
        text_input.setText(default_text)
        self.layout.addWidget(text_input)
        return text_input

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
