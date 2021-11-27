import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QWidget, QSlider,
)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QHBoxLayout Example")
        # Create a QHBoxLayout instance
        layout = QHBoxLayout()
        # Add widgets to the layout
        for i in range(0, 3):
            widget = QSlider(Qt.Vertical)
            widget.setMinimum(0)
            widget.setMaximum(250)
            widget.setSingleStep(1)
            widget.valueChanged.connect(self.value_changed)
            widget.sliderMoved.connect(self.slider_position)
            widget.sliderPressed.connect(self.slider_pressed)
            widget.sliderReleased.connect(self.slider_released)
            layout.addWidget(widget, i)
        # Set the layout on the application's window
        self.setLayout(layout)
        print(self.children())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
