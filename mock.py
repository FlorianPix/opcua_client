import functools
from random import randrange, randint

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp

import global_style
from frames.frame1.frame1 import Frame1
from frames.frame2.frame2 import Frame2
from frames.frame3.frame3 import Frame3
from frames.frame4.frame4 import Frame4
from frames.main_view.main_view import MainView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IAT control by gesture")
        self.volumes = [125, 125, 125]
        self.directions = [0, 0, 0]

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Anwendung schließen')
        exitAction.triggered.connect(qApp.quit)

        uebersichtView = QAction('&Übersicht', self)
        uebersichtView.setShortcut('Ctrl+A')
        uebersichtView.setStatusTip('Übersicht')
        uebersichtView.triggered.connect(functools.partial(self.change_frame, 0))

        umpumpenView = QAction('&Umpumpen', self)
        umpumpenView.setShortcut('Ctrl+S')
        umpumpenView.setStatusTip('Umpumpen')
        umpumpenView.triggered.connect(functools.partial(self.change_frame, 1))

        menubar = self.menuBar()
        menu = menubar.addMenu('&Menu')
        menu.addAction(exitAction)
        menu.addAction(uebersichtView)
        menu.addAction(umpumpenView)

        self.widget = MainView(self)
        self.widgets = [MainView, Frame1, Frame2, Frame3, Frame4]
        self.setCentralWidget(self.widget)

        self.statusBar().showMessage(u"Übersicht", 10000)

    def update(self):
        try:
            self.update_values()
        except:
            print("Couldn't get new values")

        window.widget.set_slider_position(0, self.volumes[0])
        window.widget.set_slider_position(1, self.volumes[1])
        window.widget.set_slider_position(2, self.volumes[2])

    def change_frame(self, widget_index, props=None):
        self.widget = self.widgets[widget_index](self)
        if props:
            self.widget.props = props
            self.widget.propify()
            if len(props) > 3:
                self.directions[props[0]] = -1
                self.directions[props[1]] = 1
        if widget_index == 0:
            self.directions = [0, 0, 0]
        self.setCentralWidget(self.widget)

    def update_values(self):
        for i in range(0, 3):
            if self.directions[i] > 0:
                if self.volumes[i] < 250:
                    self.volumes[i] += self.directions[i]
            else:
                if self.volumes[i] > 0:
                    self.volumes[i] += self.directions[i]


if __name__ == '__main__':
    app = QApplication([])
    app = global_style.set_style(app)
    window = MainWindow()
    window.resize(1920, 1080)
    window.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(window.update)
    timer.start(500)
    app.exec()

