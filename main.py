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

debug_ready = True


class RfidT(QThread):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.usage = 0
        self.threadactive = True

    RfidSignal = pyqtSignal(int)

    def __del__(self):
        self.wait()

    def run(self):
        tag = None
        self.threadactive = True
        while self.threadactive and tag is None:
            tag = backend.scan_rfid()

        if db.tagExists(tag):
            print(tag)
            print(type(tag))
            self.RfidSignal.emit(tag)
            if self.usage and db.payCoffee(str(tag)):
                backend.start_button()

        self.RfidSignal.emit(0)
        print("Rfid Thread Done..")

    def stop(self):
        self.threadactive = False
        self.wait()

class ReadyT(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.threadactive = True

    def __del__(self):
        self.wait()

    readySignal = pyqtSignal(bool)

    def run(self):
        self.threadactive = True
        while self.threadactive:
            self.readySignal.emit(backend.ready_check())
        print("closeReadyThread")
        self.stop()

    def stop(self):
        self.threadactive = False
        self.wait()

class BeansT(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.threadactive = True

    beansSignal = pyqtSignal(float, name="beansValue")

    def run(self):
        self.threadactive = True
        while self.threadactive:
            try:
                val = backend.bean_height(avg=True)
            except:
                val = 0
            self.beansSignal.emit(float(val))
            if self.threadactive:
                time.sleep(0.5)
        print("closeReadBeans")
        self.quit()

    def stop(self):
        self.threadactive = False
        self.wait()


class MainWindow(QObject):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.t = BeansT()
        self.t.beansSignal.connect(self.emitBeansValue)
        self.t1 = ReadyT()
        self.t1.readySignal.connect(self.emitReadyValue)
        self.t2 = RfidT()
        self.t2.RfidSignal.connect(self.emitRfidTag)
        self.activeTag = None
        self.ready = False
        self.cleaningType = "x"


    payingSignal = pyqtSignal(str, arguments=['paying'])
    qmlBeansSignal = pyqtSignal(float, arguments=['emitBeansValue'])
    qmlRfidSignal = pyqtSignal(str,arguments=['emitRfidTag'])
    qmlReadySignal = pyqtSignal(bool,arguments=['emitReadyValue'])

    @pyqtSlot()
    def closeRfidThread(self):
        self.t2.stop()


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
        if self.ready or debug_ready:
            self.readRfid(1)


    @pyqtSlot()
    def startReadyT(self):
        self.t1.start()

    @pyqtSlot()
    def readBeans(self):
        #dont place connect in the func do it in the init!
        self.t.start()

    def emitReadyValue(self,val):
        self.ready = val
        self.qmlReadySignal.emit(val)

    def emitBeansValue(self, val):
        print("emitbeansValue" + str(val))
        self.qmlBeansSignal.emit(val)

    @pyqtSlot()
    def closeReadBeans(self):
        self.t.stop()
        self.t1.stop()

    @pyqtSlot()
    def readRfid(self,usage):
        self.t2.usage = usage
        self.t2.start()
        #self.t2.RfidSignal.connect(self.emitRfidTag)
        print("thread rfid started")

    @pyqtSlot()
    def emitRfidTag(self, val):
        print("RfidTag " + str(val))
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
        backend.raspi_gpio_init()

        if not engine.rootObjects():
            sys.exit(-1)
        sys.exit(app.exec_())
    except (KeyboardInterrupt, SystemExit):
        backend.GPIO.cleanup()
        sys.exit()
