import functools
import random
import time
from random import randrange
from opcua import Client

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QSlider, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QAction, qApp

import global_style


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.initUI()

        self.widget = SliderTripleWidget(self)
        self.setCentralWidget(self.widget)

    def initUI(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        uebersichtView = QAction('&Übersicht', self)
        uebersichtView.setShortcut('Ctrl+A')
        uebersichtView.setStatusTip('Exit application')
        uebersichtView.triggered.connect(functools.partial(print, "Übersicht"))

        umpumpenView = QAction('&Umpumpen', self)
        umpumpenView.setShortcut('Ctrl+S')
        umpumpenView.setStatusTip('Exit application')
        umpumpenView.triggered.connect(functools.partial(print, "Umpumpen"))

        dosierenView = QAction('&Dosieren', self)
        dosierenView.setShortcut('Ctrl+D')
        dosierenView.setStatusTip('Exit application')
        dosierenView.triggered.connect(functools.partial(print, "Dosieren"))

        fuellstandView = QAction('&Füllstand', self)
        fuellstandView.setShortcut('Ctrl+F')
        fuellstandView.setStatusTip('Exit application')
        fuellstandView.triggered.connect(functools.partial(print, "Füllstand"))

        durchflussView = QAction('&Durchfluss', self)
        durchflussView.setShortcut('Ctrl+G')
        durchflussView.setStatusTip('Exit application')
        durchflussView.triggered.connect(functools.partial(print, "Durchfluss"))

        self.statusBar()

        menubar = self.menuBar()
        menu = menubar.addMenu('&Menu')
        menu.addAction(exitAction)
        menu.addAction(umpumpenView)
        menu.addAction(dosierenView)
        menu.addAction(fuellstandView)
        menu.addAction(durchflussView)


class SliderTripleWidget(QWidget):

    def __init__(self, parent):
        super(SliderTripleWidget, self).__init__(parent)
        self.sliders_widget = QWidget(self)
        self.sliders_layout = QHBoxLayout(self)
        self.labels_first_widget = QWidget(self)
        self.labels_first_layout = QHBoxLayout(self)
        self.labels_second_widget = QWidget(self)
        self.labels_second_layout = QHBoxLayout(self)
        self.layout = QVBoxLayout(self)

        self.slider0 = self.create_slider(0)
        self.slider1 = self.create_slider(1)
        self.slider2 = self.create_slider(2)
        self.sliders = [self.slider0, self.slider1, self.slider2]

        for slider in self.sliders:
            qss_path = "test.qss"
            with open(qss_path, "r") as fh:
                slider.setStyleSheet(fh.read())
            self.sliders_layout.addWidget(slider)

        self.label0 = self.create_label("Behälter 1")
        self.label1 = self.create_label("Behälter 2")
        self.label2 = self.create_label("Behälter 3")
        self.labels_first = [self.label0, self.label1, self.label2]
        self.label3 = self.create_label("0.0 mm")
        self.label4 = self.create_label("0.0 mm")
        self.label5 = self.create_label("0.0 mm")
        self.labels_second = [self.label3, self.label4, self.label5]

        for label in self.labels_first:
            qss_path = "test2.qss"
            with open(qss_path, "r") as fh:
                label.setStyleSheet(fh.read())
            self.labels_first_layout.addWidget(label)

        for label in self.labels_second:
            qss_path = "test2.qss"
            with open(qss_path, "r") as fh:
                label.setStyleSheet(fh.read())
            self.labels_second_layout.addWidget(label)

        self.sliders_widget.setLayout(self.sliders_layout)
        self.layout.addWidget(self.sliders_widget)
        self.layout.addStretch()
        self.labels_first_widget.setLayout(self.labels_first_layout)
        self.layout.addWidget(self.labels_first_widget)
        self.layout.addStretch()
        self.labels_second_widget.setLayout(self.labels_second_layout)
        self.layout.addWidget(self.labels_second_widget)
        self.setLayout(self.layout)

    def value_changed(self, nr, i):
        # print(nr)
        # print(i)
        pass

    def slider_position(self, nr, p):
        # print(nr)
        # print("position: ", p)
        pass

    def slider_pressed(self, nr):
        # print(nr)
        # print("Pressed!")
        pass

    def slider_released(self, nr):
        # print(nr)
        # print("Released")
        pass

    def set_slider_position(self, slider_nr, p):
        self.sliders[slider_nr].setValue(p)
        self.labels_second[slider_nr].setText(str(p) + " mm")

    def create_slider(self, i):
        widget = QSlider(Qt.Vertical)

        widget.setMinimum(0)
        widget.setMaximum(250)
        widget.setSingleStep(1)

        widget.valueChanged.connect(functools.partial(self.value_changed, i))
        widget.sliderMoved.connect(functools.partial(self.slider_position, i))
        widget.sliderPressed.connect(functools.partial(self.slider_pressed, i))
        widget.sliderReleased.connect(functools.partial(self.slider_released, i))
        return widget

    def create_label(self, text):
        widget = QLabel()
        widget.setText(str(text))
        widget.setAlignment(Qt.AlignCenter)
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
    return randrange(0, 250), randrange(0, 250), randrange(0, 250)


if __name__ == '__main__':
    app = QApplication([])
    app = global_style.set_style(app)
    window = MainWindow()
    window.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1000)
    app.exec()

