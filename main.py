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

    def __init__(self,u):
        QThread.__init__(self)
        self.usage = u # 1 == Coffe 0 == Cleaning

    def __del__(self):
        self.wait()

    RfidSignal = pyqtSignal(str)

    def run(self):
        tag = str(backend.scan_rfid())
        self.RfidSignal.emit(tag)
        if self.usage and db.payCoffee(tag):
                backend.start_button()
                self.RfidSignal.emit("")                     

class BeansT(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.threadactive = True

    def __del__(self):
        self.wait()

    beansSignal = pyqtSignal(float, name="beansValue")
    readySignal = pyqtSignal(bool)
    
    def run(self):

        while self.threadactive:
            try:
                val = backend.bean_height(avg=True)
            except:
                val = 0
            self.beansSignal.emit(float(val))
            self.readySignal.emit(backend.ready_check())
            time.sleep(5)
    
    def stop(self):
        print("closeReadBeans")
        self.threadactive = False
        self.wait()


class MainWindow(QObject):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.t = BeansT()
        self.activeTag = None
        self.ready = False
        self.cleaningType = "x"

    payingSignal = pyqtSignal(str, arguments=['paying'])
    qmlBeansSignal = pyqtSignal(float, arguments=['emitBeansValue'])
    qmlRfidSignal = pyqtSignal(str,arguments=['emitRfidTag'])
    qmlReadySignal = pyqtSignal(bool,arguments=['emitReadyValue'])

    @pyqtSlot()
    def cleaningMilk(self):
        print("cleaningMilkCalled")
        backend.start_button()
        db.incCleaning("Milk",self.activeTag)

    @pyqtSlot()
    def press_start(self):
        backend.start_button()

    @pyqtSlot()
    def cleaningAuth(self):
        self.readRfid(0)

    @pyqtSlot()
    def paying(self):
        print(f"Paying for Coffe: Coffeemaker is {self.ready}")
        if self.ready:
            self.readRfid(1)


    @pyqtSlot()
    def readBeans(self):
        self.t.beansSignal.connect(self.emitBeansValue)
        self.t.readySignal.connect(self.emitReadyValue)
        self.t.start()

    def emitReadyValue(self,val):
        self.ready = val
        self.qmlReadySignal.emit(val)
       
    def emitBeansValue(self, val):
        print("emitbeansValue")
        print(val)
        self.qmlBeansSignal.emit(val)

    @pyqtSlot()
    def closeReadBeans(self):
        self.t.stop()

    @pyqtSlot()
    def readRfid(self,usage):
        self.t2 = RfidT(usage)
        self.t2.RfidSignal.connect(self.emitRfidTag)
        self.t2.start()
        print("thread rfid started")

    def emitRfidTag(self, val):
        print("RfidTag" + val)
        self.activeTag = val
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