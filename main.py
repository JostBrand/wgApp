# This Python file uses the following encoding: utf-8
import sys
import os
import time

from PyQt5.QtGui import QGuiApplication, QKeySequence
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QShortcut
import database
import random
import logging


class RfidT(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    RfidSignal = pyqtSignal(str)

    def run(self):
        now = time.time()
        end = now + 30
        tag = None
        while time.time() < end:
            if tag is None:
                tag = backend.scan_rfid()
            else:
                self.RfidSignal.emit(tag)
                break
        time.sleep(10)
        self.rfidSignal.emit("")
        self.terminate()

class BeansT(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    beansSignal = pyqtSignal(float, name="beansValue")

    def run(self):

        while True:
            tmp = random.uniform(0, 1)
            self.beansSignal.emit(tmp)
            time.sleep(5)


class MainWindow(QObject):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

    payingSignal = pyqtSignal(str, arguments=['paying'])
    qmlBeansSignal = pyqtSignal(float)
    qmlRfidSignal = pyqtSignal(str)

    @pyqtSlot()
    def paying(self):
        db.payCoffee()

    @pyqtSlot()
    def readBeans(self):
        self.t = BeansT()
        self.t.beansSignal.connect(self.emitBeansValue)
        self.t.start()

    def emitBeansValue(self, val):
        print(val)
        self.qmlBeansSignal.emit(val)

    @pyqtSlot()
    def readRfid(self):
        self.t2 = RfidT()
        self.t2.RfidSignal.connect(self.emitRfidTag)
        self.t2.start()

    def emitRfidTag(self, val):
        print("RfidTag" + val)
        self.qmlRfidSignal.emit(val)


if __name__ == "__main__":
    logging.info("Application started")

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    db = database.setup()
    win = MainWindow()
    engine.rootContext().setContextProperty("Coffee", win)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
