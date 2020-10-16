# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

import database


class rfidThread(QThread):
    readTag = pyqtSignal(int)

    def run(self):
        while True:
            tmp = database.getRfidTag()
            if tmp:
                tag = tmp
            else:
                tag = None
            self.change_value.emit(tag)


class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

    payingSignal = pyqtSignal(str, arguments=['paying'])

    @pyqtSlot()
    def paying(self):
        db.payCoffee()
        self.payingSignal.emit("fun")

    def checkRFIDTrack(self):
        self.thread = rfidThread()
        self.thread.readTag.connect(self.tag)
        self.thread.start()


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    db = database.setup()
    win = MainWindow()
    engine.rootContext().setContextProperty("Coffee", win)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
