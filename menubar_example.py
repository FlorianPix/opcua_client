import functools
import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication


class basicMenubar(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 200, 200)

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
        menu.addAction(uebersichtView)
        menu.addAction(umpumpenView)
        menu.addAction(dosierenView)
        menu.addAction(fuellstandView)
        menu.addAction(durchflussView)

        self.setWindowTitle('PyQt5 Basic Menubar')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = basicMenubar()
    sys.exit(app.exec_())
