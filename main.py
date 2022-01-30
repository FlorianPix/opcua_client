import functools
import sys

from myclient import MyClient

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp
from PyQt5.QtCore import pyqtSlot

import global_style
from frames.frame1.frame1 import Frame1
from frames.frame2.frame2 import Frame2
from frames.frame3.frame3 import Frame3
from frames.frame4.frame4 import Frame4
from frames.main_view.main_view import MainView

from kinect import kinect
import threading
from queue import Queue, Empty


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
        self.hand_data = None
        self.current_widget_number = 0

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
                self.client.set('Schneider/Behaelter_A_FL', props[0]+1)
                self.client.set('Schneider/Behaelter_B_FL', props[1]+1)
                self.client.set('Schneider/Start_Umpumpen_FL', True)
        self.setCentralWidget(self.widget)
        self.current_widget_number = widget_index

    def update_values(self):
        if self.simulation:
            for i in range(0, 3):
                if self.directions[i] > 0:
                    if self.volumes[i] < 250:
                        self.volumes[i] += self.directions[i]
                        self.client.set(f'Schneider/Fuellstand{i+1}_Ist', self.volumes[i])
                else:
                    if self.volumes[i] > 0:
                        self.volumes[i] += self.directions[i]
                        self.client.set(f'Schneider/Fuellstand{i+1}_Ist', self.volumes[i])
        else:
            if self.client.sub_fuell1_ist.hasChanged():
                self.volumes[0] = int(self.client.sub_fuell1_ist.getVar())
            if self.client.sub_fuell2_ist.hasChanged():
                self.volumes[1] = int(self.client.sub_fuell2_ist.getVar())
            if self.client.sub_fuell3_ist.hasChanged():
                self.volumes[2] = int(self.client.sub_fuell3_ist.getVar())

    def update_gui(self):
        self.get_hand_data()
        if self.hand_data:
            if self.current_widget_number in [1,2]:
                area = self.hand_data["right"]["hand_area"]
                widget = self.centralWidget()
                if (not area == None and self.current_widget_number == 1 or self.current_widget_number == 2):
                    widget.highlight(area)
            if self.current_widget_number == 3:
                percent = self.hand_data["right"]["percentage"]
                self.widget.percent_to_value(percent)

    @pyqtSlot(str, str)
    def swipe_detected(self, side, direction):
        print(f"{side} Hand: {direction} swipe")
        if (side == "left"):
            if (direction == "left"):
                if self.current_widget_number in [2,3]:
                    print("returning to last screen")
                    self.change_frame(self.current_widget_number - 1, self.widget.props[0:-1])
                if self.current_widget_number in [4, 1]:
                    print("returning to main view")
                    self.change_frame(0)
            if (direction == "right"):
                if (self.current_widget_number == 0):
                    self.change_frame(1)

    @pyqtSlot(str, str)
    def hand_gesture_detected(self, side, gesture):
        print(f"{side} Hand: {gesture} detected")
        if not self.hand_data:
            return
        if (side == "right"):
            data = self.hand_data[side]
            if data["hand_gesture"][0] == "closed":
                if not data["hand_gesture"][1] == "closed":
                    if self.current_widget_number in [1,2]:
                        area = data["hand_area"]
                        print(f"selected area {area}")
                        if not area == None:
                            self.change_frame(self.current_widget_number+1, self.widget.props + [area])
                    if self.current_widget_number == 3:
                        self.widget.entered()

    def get_hand_data(self):
        try:
            self.hand_data = hand_data.get_nowait()
        except Empty as e:
            pass


def kinect_thread_runner(fps, request_status):
    game = kinect.BodyGameRuntime(fps, request_status)
    game.swipe_signal.connect(window.swipe_detected)
    game.hand_gesture_signal.connect(window.hand_gesture_detected)
    while not (game._done or done):
        game.run()
        if window.current_widget_number == 2:
            game.set_disabled_area(window.widget.props[0])
        if window.current_widget_number == 1:
            game.set_disabled_area(None)


if __name__ == '__main__':
    kinect_connected = True
    done = False

    app = QApplication([])
    app = global_style.set_style(app)
    window = MainWindow()
    if kinect_connected:
        hand_data = Queue(maxsize=1)
        kinect_thread = threading.Thread(target=kinect_thread_runner, args=(30, hand_data,))
        kinect_thread.setDaemon(False)
        kinect_thread.start()

        timer_gui = QtCore.QTimer()
        timer_gui.timeout.connect(window.update_gui)
        timer_gui.start(35)

    window.resize(1920, 1080)
    window.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(window.update)
    timer.start(1000)

    app.exec()
    done = True
