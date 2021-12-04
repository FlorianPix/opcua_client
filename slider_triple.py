import random
import time
from random import randrange
from opcua import Client

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QSlider, QApplication, QWidget, QHBoxLayout

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

        self.slider0 = self.create_slider(0)
        self.slider1 = self.create_slider(1)
        self.slider2 = self.create_slider(2)
        self.sliders = [self.slider0, self.slider1, self.slider2]

        self.layout.addWidget(self.slider0)
        self.layout.addWidget(self.slider1)
        self.layout.addWidget(self.slider2)
        self.setLayout(self.layout)

    def value_changed_0(self, i):
        # print(i)
        pass

    def value_changed_1(self, i):
        # print(i)
        pass

    def value_changed_2(self, i):
        # print(i)
        pass

    def slider_position_0(self, p):
        # print("position: ", p)
        pass

    def slider_position_1(self, p):
        # print("position: ", p)
        pass

    def slider_position_2(self, p):
        # print("position: ", p)
        pass

    def slider_pressed_0(self):
        # print("Pressed!")
        pass

    def slider_pressed_1(self):
        # print("Pressed!")
        pass

    def slider_pressed_2(self):
        # print("Pressed!")
        pass

    def slider_released_0(self):
        # print("Released")
        pass

    def slider_released_1(self):
        # print("Released")
        pass

    def slider_released_2(self):
        # print("Released")
        pass

    def set_slider_position(self, slider_nr, p):
        self.sliders[slider_nr].setValue(p)

    def create_slider(self, i):
        widget = QSlider(Qt.Vertical)

        widget.setMinimum(0)
        widget.setMaximum(250)

        widget.setSingleStep(1)

        if i == 0:
            widget.valueChanged.connect(self.value_changed_0)
            widget.sliderMoved.connect(self.slider_position_0)
            widget.sliderPressed.connect(self.slider_pressed_0)
            widget.sliderReleased.connect(self.slider_released_0)
        else:
            if i == 1:
                widget.valueChanged.connect(self.value_changed_1)
                widget.sliderMoved.connect(self.slider_position_1)
                widget.sliderPressed.connect(self.slider_pressed_1)
                widget.sliderReleased.connect(self.slider_released_1)
            else:
                widget.valueChanged.connect(self.value_changed_2)
                widget.sliderMoved.connect(self.slider_position_2)
                widget.sliderPressed.connect(self.slider_pressed_2)
                widget.sliderReleased.connect(self.slider_released_2)

        return widget


def update():
    v0 = 0
    v1 = 0
    v2 = 0

    try:
        v0, v1, v2 = get_values()
    except:
        print("Couldn't get new values")

    window.widget.set_slider_position(0, v0)
    window.widget.set_slider_position(1, v1)
    window.widget.set_slider_position(2, v2)


def get_values():
    v0 = 0
    v1 = 0
    v2 = 0
    with Client("opc.tcp://141.30.154.211:4850") as client:
        client.connect()
        client.load_type_definitions()
        root = client.get_root_node()
        objects = client.get_objects_node()
        idx = client.get_namespace_index("http://141.30.154.212:8087/OPC/DA")
        for child in root.get_children():
            if child.nodeid.Identifier == 85:
                for chil in child.get_children():
                    if chil.nodeid.Identifier == 'XML DA Server - eats11Root':
                        for chi in chil.get_children():
                            if chi.nodeid.Identifier == 'F:Schneider':
                                for ch in chi.get_children():
                                    try:
                                        if ch.nodeid.Identifier == "Schneider//Fuellstand1_Ist":
                                            v0 = int(ch.get_value())
                                        if ch.nodeid.Identifier == "Schneider//Fuellstand2_Ist":
                                            v1 = int(ch.get_value())
                                        if ch.nodeid.Identifier == "Schneider//Fuellstand3_Ist":
                                            v2 = int(ch.get_value())
                                    except:
                                        pass
        print(v0, v1, v2)
        return v0, v1, v2


if __name__ == '__main__':
    app = QApplication([])
    app = global_style.set_style(app)
    window = MainWindow()
    window.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(10000)  # every 10,000 milliseconds
    app.exec()

