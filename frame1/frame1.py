import functools

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSlider, QWidget, QHBoxLayout, QVBoxLayout


class Frame1(QWidget):

    def __init__(self, parent):
        super(Frame1, self).__init__(parent)
        self.sliders_widget = QWidget(self)
        self.sliders_layout = QHBoxLayout(self)
        self.info_widget = QWidget(self)
        self.info_layout = QHBoxLayout(self)
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
            qss_path = "frame1/slider.qss"
            with open(qss_path, "r") as fh:
                slider.setStyleSheet(fh.read())
            self.sliders_layout.addWidget(slider)

        text_path = "frame1/text_frame1.txt"
        with open(text_path, "r", encoding='utf8') as fh:
            self.info_field = self.create_label(fh.read())
            qss_path = "frame1/label.qss"
            with open(qss_path, "r") as fh2:
                self.info_field.setStyleSheet(fh2.read())
                self.info_layout.addWidget(self.info_field)

        self.labels_first = [self.create_label("Behälter 1"), self.create_label("Behälter 2"), self.create_label("Behälter 3")]
        self.labels_second = [self.create_label("0.0 mm"), self.create_label("0.0 mm"), self.create_label("0.0 mm")]

        for label in self.labels_first:
            qss_path = "frame1/label.qss"
            with open(qss_path, "r") as fh:
                label.setStyleSheet(fh.read())
            self.labels_first_layout.addWidget(label)

        for label in self.labels_second:
            qss_path = "frame1/label.qss"
            with open(qss_path, "r") as fh:
                label.setStyleSheet(fh.read())
            self.labels_second_layout.addWidget(label)

        self.sliders_widget.setLayout(self.sliders_layout)
        self.layout.addWidget(self.sliders_widget)
        self.info_widget.setLayout(self.info_layout)
        self.layout.addWidget(self.info_widget)
        self.labels_first_widget.setLayout(self.labels_first_layout)
        self.layout.addWidget(self.labels_first_widget)
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
        font = QtGui.QFont()
        font.setPointSize(36)
        widget = QLabel()
        widget.setText(str(text))
        widget.setFont(font)
        widget.setAlignment(Qt.AlignCenter)
        return widget
