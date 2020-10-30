# This Python file uses the following encoding: utf-8
import logging
import os
import sys
import time
from collections import deque
from datetime import datetime, timedelta

import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

import backend
import database

debug_ready = True


# Communication Thread to RFID Reader
class RfidT(QThread):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)


    RfidSignal = pyqtSignal(str)

    def __del__(self):
        self.wait()

    def run(self):
        self.threadactive = True
        tag = None

        while self.threadactive and tag is None:
            tag = backend.scan_rfid()

        if db.tagExists(tag):
            tag = str(tag)
            self.RfidSignal.emit(tag)
            if self.usage is "Coffee" and db.payCoffee(str(tag)):
                # if self.usage is 1:
                backend.start_button()
                self.RfidSignal.emit("")
            elif self.usage is "TaskStatus":
                win.checkTask(tag)

        print("Rfid Thread Done..")


# Checks the ready LED - 3 states: off, blinking, on
class ReadyT(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    readySignal = pyqtSignal(bool)

    def run(self):
        self.threadactive = True
        while self.threadactive:
            self.readySignal.emit(backend.ready_check())
        print("closeReadyThread")

    def stop(self):
        self.threadactive = False



# Reading an ultrasonic sensor to show bean height in gui
class BeansT(QThread):

    def __init__(self):
        QThread.__init__(self)


    beansSignal = pyqtSignal(float, name="beansValue")

    def run(self):
        self.threadactive = True
        while self.threadactive:
            try:
                val = backend.bean_height(avg=True)
            except:
                val = -1
                print("BeansT val = -1\n")

            if val is not -1:
                self.beansSignal.emit(float(val))
            if self.threadactive:
                time.sleep(1.5)
        print("Beans Thread closed")

    def stop(self):
        self.threadactive = False


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
        self.lastTag = None
        self.ready = False
        self.tasks = False
        self.cleaningType = "x"
        self.tasks = [{"take out recycling": "Pictures/Tasks/recycling.jpg"},
                      {"shopping": "Pictures/Tasks/shopping.jpg"},
                      {"taking trash out": "Pictures/Tasks/trash.jpg"},
                      {"washing the towels": "Pictures/Tasks/towel.jpg"},
                      {"vacuum hall and clean kitchen": "Pictures/Tasks/vacuum.jpg"}]

    payingSignal = pyqtSignal(str, arguments=['paying'])
    qmlBeansSignal = pyqtSignal(float, arguments=['emitBeansValue'])
    qmlRfidSignal = pyqtSignal(str, arguments=['emitRfidTag'])
    qmlReadySignal = pyqtSignal(bool, arguments=['emitReadyValue'])
    qmlBalanceSignal = pyqtSignal(float, arguments=['emitBalanceValue'])
    qmlTasksSignal = pyqtSignal(int, str, str, bool, int,
                                arguments=["groupId", "taskString", "picturePath", "checked", "weekDates"])

    @pyqtSlot(str, int)
    @pyqtSlot(str, bool)
    @pyqtSlot(str, str)
    def setter(self, var, val):
        setattr(self, var, val)
        print(var, val)

    def checkTask(self, tag):
        print(f'RfidTag for checkTask {tag}')
        group_id = db.getGroupId(tag)
        print(f'GroupNr: {group_id}')
        if group_id is not None:
            db.checkTask(group_id)
            self.setTasks()
            self.qmlTasksSignal.emit(-1, "reload", "", False, "")

    @pyqtSlot()
    def setTasks(self):
        week_of_year = datetime.today().isocalendar()[1]
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        print("Today: " + str(today))
        print("Start: " + str(start))
        print("End: " + str(end))
        week_dates = f'{start}-{end}'

        copyTasks = deque(self.tasks)
        copyTasks.rotate(week_of_year - 3)
        for id, taskDict in enumerate(list(copyTasks)):
            for taskName, picturePath in taskDict.items():
                print(f"{id+1} Name: {taskName} {db.getTasksStatus(id+1)} \n")
                self.qmlTasksSignal.emit(id + 1, taskName, picturePath, db.getTasksStatus(id+1), week_dates)

    @pyqtSlot()
    def closeRfidThread(self):
        self.t2.threadactive = False

    @pyqtSlot()
    def setBalanceText(self):
        if self.activeTag is not None:
            self.qmlBalanceSignal.emit(np.around(float(db.getAccountBalance(str(self.activeTag))), decimals=2))

    @pyqtSlot()
    def cleaningMilk(self):
        print(f"{db.getAccountName(self.activeTag)}  {self.activeTag} has cleaned the milk tank")
        backend.start_button()
        db.incCleaning("Milk", self.activeTag)
        self.activeTag = None

    @pyqtSlot()
    def cleaning(self, cleaningtype):
        if cleaningtype == "Milk":
            print(f"{db.getAccountName(self.activeTag)}  {self.activeTag} has cleaned the milk tank")
            backend.start_button()
            db.incCleaning("Milk", self.activeTag)
            self.activeTag = None
        else:
            self.cleaningType = cleaningtype

    @pyqtSlot()
    def refund(self):
        if self.lastTag is None:
            return
        print(f'{db.getAccountName(self.lastTag)} got a refund.')
        db.changeValue(self.lastTag, "Amount", db.getAccountBalance(self.lastTag) + 0.35)
        db.systemlogger("Refund claimed", self.lastTag)
        db.incRefund(self.lastTag)

    @pyqtSlot()
    def incCleaning(self):
        print(f"{db.getAccountName(self.activeTag)} has done a {self.cleaningType} cleaning.")
        db.incCleaning(self.cleaningType, self.activeTag)
        if self.cleaningType == "Lime":
            cleaningReward = 2
        elif self.cleaningType == "Full":
            cleaningReward = 2
        else:
            cleaningReward = 0

        #db.changeAmount(self.activeTag, db.getAccountBalance(self.activeTag) + cleaningReward)
        db.changeValue(self.lastTag, "Amount", db.getAccountBalance(self.lastTag) + cleaningReward)
        self.activeTag = None

    @pyqtSlot()
    def press_start(self):
        backend.start_button()

    @pyqtSlot()
    def call_reset(self):
        backend.RFID_reset()

        #self.t.terminate()

    # Adds 10€ to ActiveRfidTag to the database and emit Signal to GUI to show balance
    @pyqtSlot()
    def confirmRefill(self):
        db.changeValue(str(self.activeTag),"Amount", str(float(db.getAccountBalance(str(self.activeTag)) + 10)))
        print(f"{db.getAccountName(str(self.activeTag))} has refilled the coffee. Thank You.")
        self.qmlBalanceSignal.emit(np.around(float(db.getAccountBalance(str(self.activeTag))), decimals=2))

    # Authentication for Coffee,Refill, Cleaning or the weekly tasks
    @pyqtSlot(str)
    def Auth(self, reason):
        if reason == "Cleaning":
            self.readRfid("Cleaning")
        elif reason == "Refill":
            self.readRfid("Refill")
        elif reason == "Coffee":
            print(f"Coffeemaker is {self.ready}")
            if self.ready or debug_ready:
                self.readRfid("Coffee")
        elif reason == "TaskStatus":
            self.readRfid("TaskStatus")

    @pyqtSlot()
    def startReadyT(self):
        if not self.t1.isRunning():
            self.t1.start()

    @pyqtSlot()
    def readBeans(self):
        # dont place connect in the func do it in the init!
        if not self.t.isRunning():
            self.t.start()

    def emitReadyValue(self, val):
        self.ready = val
        self.qmlReadySignal.emit(val)

    def emitBeansValue(self, val):
        #print("Beans Height:" + str(val) + "\n")
        self.qmlBeansSignal.emit(val)


    @pyqtSlot()
    def closeReadBeans(self):
        if self.t.isRunning():
            self.t.stop()
        if self.t1.isRunning():
            self.t1.stop()

    @pyqtSlot()
    def readRfid(self, usage):
        self.t2.usage = usage
        if not self.t2.isRunning():
            self.t2.start()
            print("RFID Thread started.")

    def emitRfidTag(self, val):
        if len(val) > 3:
            print(f"RFID-Tag: {str(val)} ({db.getAccountName(val)}) logged in.")
        self.activeTag = val
        if self.activeTag is not "":
            self.lastTag = self.activeTag

        self.qmlRfidSignal.emit(str(val))


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
