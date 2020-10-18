# coffeeberry
# functions for reading RFID TAG, Bean height (ultrasonic), AD Converter Voltage photoresistor
# and switching RELAIS

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD) # GPIO Nummern statt Board Nummern
GPIO.setwarnings(False)
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
from ADS1x15 import ADS1015
import numpy as np


def start_button():
    RELAIS_1_GPIO = 35
    RELAIS_2_GPIO = 37

    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen
    GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Modus zuweisen


    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # Relais schaltet bei LOW Signal
    GPIO.output(RELAIS_2_GPIO, GPIO.LOW) #
    time.sleep(0.5)
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # an
    GPIO.output(RELAIS_2_GPIO, GPIO.HIGH)
    print("Start Knopf gedrückt")

    GPIO.cleanup()

def scan_rfid():
    print("RFID Scan gestartet, Chip jetzt vorhalten")
    scanning=1
    while scanning==1:
        output = reader.read()
        #print(reader.read())
        if output is not None:
            scanning=0
    return output[0]

def bean_height(avg=False,relative=True):
    TRIG=29
    ECHO=31

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    if avg==False:
        readings=1
    else:
        readings=5

    if relative==True:
        MAX=8.6
        MIN=2.0
        dif = MAX-MIN

        total=0
        for i in range(0,readings):

            GPIO.output(TRIG, True)
            time.sleep(0.0001)
            GPIO.output(TRIG,False)
            while GPIO.input(ECHO)==False:
                start = time.time()
            while GPIO.input(ECHO)==True:
                end = time.time()
            sigtime= end-start
            total = total+sigtime
            time.sleep(0.05)

        averaged = total/readings

        distance = averaged/0.000058
        distance = distance-MIN
        rel = distance/dif
        rel = 1-rel
        print(rel)
        distance=rel*100

    else:

        total=0
        for i in range(0,readings):

            GPIO.output(TRIG, True)
            time.sleep(0.0001)
            GPIO.output(TRIG,False)
            while GPIO.input(ECHO)==False:
                start = time.time()
            while GPIO.input(ECHO)==True:
                end = time.time()
            sigtime= end-start
            total = total+sigtime
            time.sleep(0.05)

        averaged = total/readings

        distance = averaged/0.000058
        print("Distance: {} cm".format(distance))

    return np.around(distance,decimals=0)
    GPIO.cleanup()

def ready_check():
    adc = ADS1015()
    GAIN = 1
    READY=False

    # Main loop.
    measures=[0]*3
    x=0
    while True:
        values = [0]*4
        for i in range(4):
            values[i] = adc.read_adc(i, gain=GAIN)

        measures[x]=values[2]
        x=x+1
        if x==2:
            x=0

        print("milliVolts")
        print(measures[0], measures[1])
        print(np.abs(measures[0]-measures[1]))

        if np.abs(measures[0]-measures[1]) <=200 and measures[0] >=1000:
            print("System betriebsbereit")
            READY=True
        else:
            print("System nicht betriebsbereit")
            READY=False
            pass

        if READY==True:
            checkcount=checkcount+1
            if checkcount>=3:
                print(checkcount)
                finalready=True
                checkcount=0
        else:
            checkcount=0

        time.sleep(0.5)
        ## Knopf SETZEN
        ## if READY==TRUE:
        ## KNOPF SHOW
        ## ELSE: nicht show

    return READY
    GPIO.cleanup()

#beanheight=bean_height(avg=True)
#print(beanheight)
#ready= ready_check()
print(scan_rfid())
#start_button()
