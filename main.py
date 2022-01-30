import sys
import time
import functools
import sys

from myclient import MyClient
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
        self.directions = [0, 0, 0]
        self.volumes = [125, 125, 125]
        self.props = []
        self.simulation = True
        try:
            self.client = MyClient()
        except BaseException as err:
            print(err)
            sys.exit()

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

    def __del__(self):
        if hasattr(self, 'client'):
            self.client.set('Schneider/Start_Umpumpen_FL', False)
            self.client.client.disconnect()

    def update(self):
        try:
            self.update_values()
        except BaseException as err:
            print("Couldn't get new values")
            print(err)
        if self.client.node_dict['Schneider/Start_Umpumpen_FL'].get_value() and len(self.props) > 3:
            if self.volumes[self.props[0]] <= self.props[3] - self.props[2]:
                self.client.set('Schneider/Start_Umpumpen_FL', False)
                self.change_frame(0)
            if self.volumes[self.props[1]] >= self.props[4] + self.props[2]:
                self.client.set('Schneider/Start_Umpumpen_FL', False)
                self.change_frame(0)
        window.widget.set_slider_position(0, self.volumes[0])
        window.widget.set_slider_position(1, self.volumes[1])
        window.widget.set_slider_position(2, self.volumes[2])

    def change_frame(self, widget_index, props=None):
        self.widget = self.widgets[widget_index](self)
        if widget_index == 0:
            self.client.set('Schneider/Start_Umpumpen_FL', False)
            self.directions = [0, 0, 0]
        elif props:
            self.widget.props = props
            self.widget.propify()
            if len(props) > 3:
                self.props = props
                if self.simulation:
                    self.directions[props[0]] = -1
                    self.directions[props[1]] = 1
                else:
                    self.client.set('Schneider/Behaelter_A_FL', props[0]+1)
                    self.client.set('Schneider/Behaelter_B_FL', props[1]+1)
                    self.client.set('Schneider/Start_Umpumpen_FL', True)
        self.setCentralWidget(self.widget)

    def update_values(self):
        if self.simulation:
            for i in range(0, 3):
                if self.directions[i] > 0:
                    if self.volumes[i] < 250:
                        self.volumes[i] += self.directions[i]
                else:
                    if self.volumes[i] > 0:
                        self.volumes[i] += self.directions[i]
        else:
            if self.client.sub_fuell1_ist.hasChanged():
                self.volumes[0] = int(self.client.sub_fuell1_ist.getVar())
            if self.client.sub_fuell2_ist.hasChanged():
                self.volumes[1] = int(self.client.sub_fuell2_ist.getVar())
            if self.client.sub_fuell3_ist.hasChanged():
                self.volumes[2] = int(self.client.sub_fuell3_ist.getVar())


if __name__ == '__main__':
    app = QApplication([])
    app = global_style.set_style(app)
    window = MainWindow()
    window.resize(1920, 1080)
    window.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(window.update)
    timer.start(1000)
    app.exec()



