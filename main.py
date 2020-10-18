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
import backend

class RfidT(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    RfidSignal = pyqtSignal(str)

    def run(self):
        now = time.time()
        end = now + 30
        tag = str(backend.scan_rfid())
        self.RfidSignal.emit(tag)
        if db.payCoffee(tag):
            backend.start_button()
    
    def stop(self):
        backend.GPIO.cleanup()
        self.stop()
        self.wait()

class BeansT(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.threadactive = True

    def __del__(self):
        self.wait()

    beansSignal = pyqtSignal(float, name="beansValue")
    
    def run(self):

        while self.threadactive:
            tmp = float(backend.bean_height(avg=True))
            self.beansSignal.emit(tmp)
            time.sleep(5)
    
    def stop(self):
        print("closeReadBeans")
        self.threadactive = False
        self.wait()


class MainWindow(QObject):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.t = BeansT()

    payingSignal = pyqtSignal(str, arguments=['paying'])
    qmlBeansSignal = pyqtSignal(float, arguments=['emitBeansValue'])
    qmlRfidSignal = pyqtSignal(str,arguments=['emitRfidTag'])


    @pyqtSlot()
    def paying(self):
        self.readRfid()

    @pyqtSlot()
    def readBeans(self):
        self.t.beansSignal.connect(self.emitBeansValue)
        self.t.start()

    def emitBeansValue(self, val):
        #print("bean height returned: "+str(val))
        print("emitbeansValue")
        print(val)
        self.qmlBeansSignal.emit(val)

    @pyqtSlot()
    def closeReadBeans(self):
        self.t.stop()

    @pyqtSlot()
    def readRfid(self):
        self.t2 = RfidT()
        self.t2.RfidSignal.connect(self.emitRfidTag)
        self.t2.start()
        print("thread rfid started")

    def emitRfidTag(self, val):
        print("RfidTag" + val)
        self.qmlRfidSignal.emit(val)




if __name__ == "__main__":
    try:
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
    except (KeyboardInterrupt, SystemExit):
        
        sys.exit()
