import time
from random import randrange

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QSlider, QApplication, QVBoxLayout, QWidget, QHBoxLayout

import global_style


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.widget = SliderTripleWidget(self)
        self.setCentralWidget(self.widget)


class SliderTripleWidget(QWidget):

    def __init__(self, parent):
        super(SliderTripleWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        self.slider1 = self.create_slider()
        self.layout.addWidget(self.slider1)
        self.slider2 = self.create_slider()
        self.layout.addWidget(self.slider2)
        self.slider3 = self.create_slider()
        self.layout.addWidget(self.slider3)

        self.setLayout(self.layout)

    def value_changed(self, i):
        print(i)

    def slider_position(self, p):
        print("position", p)

    def slider_pressed(self):
        print("Pressed!")

    def slider_released(self):
        print("Released")

    def set_slider_position(self, p):
        self.slider1.setValue(p)

    def create_slider(self):
        widget = QSlider(Qt.Vertical)

        widget.setMinimum(0)
        widget.setMaximum(250)

        widget.setSingleStep(1)

        widget.valueChanged.connect(self.value_changed)
        widget.sliderMoved.connect(self.slider_position)
        widget.sliderPressed.connect(self.slider_pressed)
        widget.sliderReleased.connect(self.slider_released)

        return widget


if __name__ == '__main__':
    app = QApplication([])
    app = global_style.set_style(app)
    window = MainWindow()
    window.show()

    def update():
        value = int(randrange(0, 250))
        window.widget.set_slider_position(value)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1000)  # every 10,000 milliseconds
    app.exec()

