import functools
from random import randrange, randint

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
        self.hand_data = None
        self.current_widget_number = 0

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
        print(props)
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
        self.current_widget_number = widget_index        

    def update_values(self):
        for i in range(0, 3):
            if self.directions[i] > 0:
                if self.volumes[i] < 250:
                    self.volumes[i] += self.directions[i]
            else:
                if self.volumes[i] > 0:
                    self.volumes[i] += self.directions[i]

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
        #if not self.hand_data:
        #    print("waiting for data")
        #    self.hand_data = hand_data.get()
        try:
            self.hand_data = hand_data.get_nowait()
        except Empty as e:
            pass


def kinect_thread_runner(fps, request_status):
    game = kinect.BodyGameRuntime(fps, request_status);
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
    hand_data = Queue(maxsize=1)
    app = QApplication([])
    app = global_style.set_style(app)
    window = MainWindow()
    if kinect_connected:
        kinect_thread = threading.Thread(target=kinect_thread_runner, args=(30, hand_data,))
        kinect_thread.setDaemon(False)
        kinect_thread.start()

  
    window.resize(1920, 1080)
    window.show()

    timer_opcua = QtCore.QTimer()
    timer_opcua.timeout.connect(window.update)
    timer_opcua.start(500)

    timer_gui = QtCore.QTimer()
    timer_gui.timeout.connect(window.update_gui)
    timer_gui.start(35)


    app.exec()
    done = True

