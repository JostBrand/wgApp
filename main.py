# This Python file uses the following encoding: utf-8
import sys
import os
import time

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

import database
import random

import backend

class BeansT(QThread):

    def __init__(self):
     QThread.__init__(self)

     def __del__(self):
         self.wait()

    beansSignal = pyqtSignal(float,name="beansValue")
    def run(self):

        while True:
            tmp = float(backend.bean_height(avg=True))
            #tmp = float(random.uniform(0,1))
            #print("bean height returned: "+str(tmp))
            self.beansSignal.emit(tmp)
            time.sleep(5)


class MainWindow(QObject):

    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)

    payingSignal = pyqtSignal(str, arguments=['paying'])
    qmlBeansSignal = pyqtSignal(float, arguments=['emitBeansValue'])
    
    @pyqtSlot()
    def paying(self):
        db.payCoffee()

    @pyqtSlot()
    def readBeans(self):
        self.t = BeansT()
        self.t.beansSignal.connect(self.emitBeansValue)
        self.t.start()
        print("started readBeans Thread")


    def emitBeansValue(self, val):
        #print("bean height returned: "+str(val))
        print("emitbeansValue")
        print(val)
        self.qmlBeansSignal.emit(val)


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
