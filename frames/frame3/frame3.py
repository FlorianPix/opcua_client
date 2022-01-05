import functools
import re

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSlider, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit


class Frame3(QWidget):
    def __init__(self, parent):
        super(Frame3, self).__init__(parent)
        self.parent = parent
        self.props = []
        self.chosen_sliders = []
        self.chosen_name_labels = []
        self.chosen_labels = []
        self.sliders_widget = QWidget(self)
        self.sliders_layout = QHBoxLayout(self)
        self.info_widget = QWidget(self)
        self.info_layout = QHBoxLayout(self)
        self.static_labels_widget = QWidget(self)
        self.static_labels_layout = QHBoxLayout(self)
        self.name_labels_widget = QWidget(self)
        self.name_labels_layout = QHBoxLayout(self)
        self.labels_widget = QWidget(self)
        self.labels_layout = QHBoxLayout(self)
        self.target_widget = QWidget(self)
        self.target_layout = QHBoxLayout(self)
        self.abort_widget = QWidget(self)
        self.abort_layout = QHBoxLayout(self)
        self.layout = QVBoxLayout(self)

        self.sliders = [self.create_slider(0), self.create_slider(1), self.create_slider(2)]
        text_path = "frames/frame3/text_frame3.txt"
        with open(text_path, "r", encoding='utf8') as fh:
            self.info_field = self.create_label(fh.read())
        self.static_labels = [self.create_label("Startbehälter"), self.create_label("Zielbehälter")]
        self.name_labels = [self.create_label("Behälter 1"), self.create_label("Behälter 2"), self.create_label("Behälter 3")]
        self.labels = [self.create_label("0.0 mm"), self.create_label("0.0 mm"), self.create_label("0.0 mm")]
        self.target_prefix = self.create_label("Soll")
        self.target = self.create_edit()
        self.target_postfix = self.create_label("mm")
        self.abort = self.create_button("Abbrechen")

    def propify(self):
        for i in self.props[0:2]:
            self.chosen_sliders.append(self.sliders[i])
            self.chosen_name_labels.append(self.name_labels[i])
            self.chosen_labels.append(self.labels[i])

        for slider in self.chosen_sliders:
            qss_path = "frames/frame3/slider.qss"
            with open(qss_path, "r") as fh:
                slider.setStyleSheet(fh.read())
            self.sliders_layout.addWidget(slider)

        for label in self.static_labels:
            qss_path = "frames/frame3/label.qss"
            with open(qss_path, "r") as fh:
                label.setStyleSheet(fh.read())
            self.static_labels_layout.addWidget(label)

        qss_path = "frames/frame2/label.qss"
        with open(qss_path, "r") as fh2:
            self.info_field.setStyleSheet(fh2.read())
            self.info_layout.addWidget(self.info_field)

        for label in self.chosen_name_labels:
            qss_path = "frames/frame3/label.qss"
            with open(qss_path, "r") as fh:
                label.setStyleSheet(fh.read())
            self.name_labels_layout.addWidget(label)

        for label in self.chosen_labels:
            qss_path = "frames/frame3/label.qss"
            with open(qss_path, "r") as fh:
                label.setStyleSheet(fh.read())
            self.labels_layout.addWidget(label)

        qss_path = "frames/frame3/label.qss"
        with open(qss_path, "r") as fh:
            self.target_prefix.setStyleSheet(fh.read())
            self.target_layout.addWidget(self.target_prefix)

        qss_path = "frames/frame3/edit.qss"
        with open(qss_path, "r") as fh:
            self.target.setStyleSheet(fh.read())
            self.target_layout.addWidget(self.target)

        qss_path = "frames/frame3/label.qss"
        with open(qss_path, "r") as fh:
            self.target_postfix.setStyleSheet(fh.read())
            self.target_layout.addWidget(self.target_postfix)

        qss_path = "frames/frame3/button.qss"
        with open(qss_path, "r") as fh:
            self.abort.setStyleSheet(fh.read())
            self.abort_layout.addWidget(self.abort)

        self.sliders_widget.setLayout(self.sliders_layout)
        self.layout.addWidget(self.sliders_widget)
        self.info_widget.setLayout(self.info_layout)
        self.layout.addWidget(self.info_widget)
        self.static_labels_widget.setLayout(self.static_labels_layout)
        self.layout.addWidget(self.static_labels_widget)
        self.name_labels_widget.setLayout(self.name_labels_layout)
        self.layout.addWidget(self.name_labels_widget)
        self.labels_widget.setLayout(self.labels_layout)
        self.layout.addWidget(self.labels_widget)
        self.target_widget.setLayout(self.target_layout)
        self.layout.addWidget(self.target_widget)
        self.abort_widget.setLayout(self.abort_layout)
        self.layout.addWidget(self.abort_widget)
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
        self.labels[slider_nr].setText(str(p) + " mm")

    def create_slider(self, i):
        widget = QSlider(Qt.Vertical)

        widget.setMinimum(0)
        widget.setMaximum(250)
        widget.setSingleStep(1)
        widget.setValue(self.parent.volumes[i])

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

    def create_edit(self):
        font = QtGui.QFont()
        font.setPointSize(36)
        widget = QLineEdit()
        widget.setFont(font)
        widget.setAlignment(Qt.AlignRight)
        widget.returnPressed.connect(self.entered)
        widget.textEdited.connect(self.text_changed)
        return widget

    def entered(self):
        try:
            content = int(self.target.text())
            if len(self.props) == 3:
                try:
                    self.props[2] = content
                except ValueError as err:
                    print(err)
            else:
                try:
                    self.props.append(content)
                except ValueError as err:
                    print(err)
            if self.chosen_sliders[0].value() - content >= 0:
                if self.chosen_sliders[1].value() + content <= 250:
                    self.props.append(self.chosen_sliders[0].value())
                    self.props.append(self.chosen_sliders[1].value())
                    self.parent.change_frame(4, props=self.props)
                else:
                    print("Im Zielbehälter ist nicht genügend Platz für das angegebene Soll.")
            else:
                print("Im Startbehälter ist nicht genügend Flüssigkeit für das angegebene Soll.")
        except ValueError as err:
            correction = re.sub("[^0-9]", "", self.target.text())
            self.target.setText(correction)

    def text_changed(self, text):
        if len(self.props) == 3:
            try:
                self.props[2] = int(text)
            except ValueError as err:
                pass
        else:
            try:
                self.props.append(int(text))
            except ValueError as err:
                pass

    def create_button(self, text):
        font = QtGui.QFont()
        font.setPointSize(36)
        widget = QPushButton()
        widget.setText(str(text))
        widget.setFont(font)
        widget.clicked.connect(lambda: self.parent.change_frame(0))
        return widget


