import functools

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSlider, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit


class Frame4(QWidget):
    def __init__(self, parent):
        super(Frame4, self).__init__(parent)
        self.parent = parent
        self.props = []
        self.chosen_sliders = []
        self.chosen_name_labels = []
        self.chosen_labels = []
        self.sliders_widget = QWidget(self)
        self.sliders_layout = QHBoxLayout(self)
        self.static_labels_widget = QWidget(self)
        self.static_labels_layout = QHBoxLayout(self)
        self.name_labels_widget = QWidget(self)
        self.name_labels_layout = QHBoxLayout(self)
        self.labels_widget = QWidget(self)
        self.labels_layout = QHBoxLayout(self)
        self.target_widget = QWidget(self)
        self.target_layout = QHBoxLayout(self)
        self.actual_widget = QWidget(self)
        self.actual_layout = QHBoxLayout(self)
        self.abort_widget = QWidget(self)
        self.abort_layout = QHBoxLayout(self)
        self.layout = QVBoxLayout(self)

        self.sliders = [self.create_slider(0), self.create_slider(1), self.create_slider(2)]
        self.static_labels = [self.create_label("Startbehälter"), self.create_label("Zielbehälter")]
        self.name_labels = [self.create_label("Behälter 1"), self.create_label("Behälter 2"), self.create_label("Behälter 3")]
        self.labels = [self.create_label("0.0 mm"), self.create_label("0.0 mm"), self.create_label("0.0 mm")]
        self.target_prefix = self.create_label("Soll")
        self.target = self.create_edit()
        self.target_postfix = self.create_label("mm")
        self.actual_prefix = self.create_label("Ist")
        self.actual = self.create_edit()
        self.actual_postfix = self.create_label("mm")
        self.abort = self.create_button("Beenden")

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
            qss_path = "frames/frame4/label.qss"
            with open(qss_path, "r") as fh:
                label.setStyleSheet(fh.read())
            self.static_labels_layout.addWidget(label)

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

        qss_path = "frames/frame4/label.qss"
        with open(qss_path, "r") as fh:
            self.target_prefix.setStyleSheet(fh.read())
            self.target_layout.addWidget(self.target_prefix)

        qss_path = "frames/frame4/edit.qss"
        with open(qss_path, "r") as fh:
            self.target.setStyleSheet(fh.read())
            self.target.setText(str(self.props[2]))
            self.target_layout.addWidget(self.target)

        qss_path = "frames/frame4/label.qss"
        with open(qss_path, "r") as fh:
            self.target_postfix.setStyleSheet(fh.read())
            self.target_layout.addWidget(self.target_postfix)

        qss_path = "frames/frame4/label.qss"
        with open(qss_path, "r") as fh:
            self.actual_prefix.setStyleSheet(fh.read())
            self.actual_layout.addWidget(self.actual_prefix)

        qss_path = "frames/frame4/edit.qss"
        with open(qss_path, "r") as fh:
            self.actual.setStyleSheet(fh.read())
            self.actual.setText("0")
            self.actual_layout.addWidget(self.actual)

        qss_path = "frames/frame4/label.qss"
        with open(qss_path, "r") as fh:
            self.actual_postfix.setStyleSheet(fh.read())
            self.actual_layout.addWidget(self.actual_postfix)

        qss_path = "frames/frame4/button.qss"
        with open(qss_path, "r") as fh:
            self.abort.setStyleSheet(fh.read())
            self.abort_layout.addWidget(self.abort)

        self.sliders_widget.setLayout(self.sliders_layout)
        self.layout.addWidget(self.sliders_widget)
        self.static_labels_widget.setLayout(self.static_labels_layout)
        self.layout.addWidget(self.static_labels_widget)
        self.name_labels_widget.setLayout(self.name_labels_layout)
        self.layout.addWidget(self.name_labels_widget)
        self.labels_widget.setLayout(self.labels_layout)
        self.layout.addWidget(self.labels_widget)
        self.target_widget.setLayout(self.target_layout)
        self.layout.addWidget(self.target_widget)
        self.actual_widget.setLayout(self.actual_layout)
        self.layout.addWidget(self.actual_widget)
        self.abort_widget.setLayout(self.abort_layout)
        self.layout.addWidget(self.abort_widget)
        self.parent.statusBar().showMessage(u"Umpumpen gestartet", 10000)
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
        if slider_nr == self.props[0]:
            target = self.props[3] - self.props[2]
            diff = target - self.chosen_sliders[0].value()
            text = self.props[2] + diff
            self.actual.setText(str(text))
            if abs(diff) <= 0:
                self.parent.statusBar().showMessage(u"Umpumpen beendet", 10000)
                self.parent.change_frame(0)

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
        widget.setReadOnly(True)
        return widget

    def create_button(self, text):
        font = QtGui.QFont()
        font.setPointSize(36)
        widget = QPushButton()
        widget.setText(str(text))
        widget.setFont(font)
        widget.clicked.connect(lambda: self.parent.change_frame(0))
        return widget
