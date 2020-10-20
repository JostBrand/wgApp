# coffeeberry
# functions for reading RFID TAG, Bean height (ultrasonic), AD Converter Voltage photoresistor
# and switching RELAIS

import RPi.GPIO as GPIO
import time

#GPIO.setwarnings(False)
from mfrc522 import SimpleMFRC522

from ADS1x15 import ADS1015
import numpy as np

RELAIS_1_GPIO = 35
RELAIS_2_GPIO = 37

TRIG=29
ECHO=31



def raspi_gpio_init():
    GPIO.setmode(GPIO.BOARD) # GPIO Nummern statt Board Nummern


    #GPIO.setwarnings(False)
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen
    GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Modus zuweisen


    #rfid object
    #reader = SimpleMFRC522()

    #own Reader



    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)



def start_button():

    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # Relais schaltet bei LOW Signal
    GPIO.output(RELAIS_2_GPIO, GPIO.LOW) #
    time.sleep(0.5)
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # an
    GPIO.output(RELAIS_2_GPIO, GPIO.HIGH)
    print("Start Knopf gedrückt")

    #GPIO.cleanup()

class MyReader(SimpleMFRC522):
    def __init__(self, *args, **kwargs):
        super(MyReader, self).__init__(*args, **kwargs)

    def read(self):
      x=0
      id, text = self.read_no_block()
      while not id and x < 4:
          id, text = self.read_no_block()
          x+=1
      return id, text


    def read_id(self):
        id = self.read_id_no_block()
        x = 0
        while not id and x <4:
            print(x)
            id = self.read_id_no_block()
            x +=1
        return id

reader2 = MyReader()

def scan_rfid():
    print("RFID Scan gestartet, Chip jetzt vorhalten")
    output = reader2.read()
    return output[0]

def bean_height(avg=False,relative=True):


    #GPIO.setmode(GPIO.BOARD)

    if avg is False:
        readings=1
    else:
        readings=5

    if relative is True:
        MAX=8.6
        MIN=2.0
        dif = MAX-MIN

        total=0
        for _ in range(0,readings):
            GPIO.output(TRIG,False)
            time.sleep(0.5)
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
        #print(rel)
        distance=rel
        if distance<=0:
            distance=0

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

    #GPIO.cleanup()
    return np.around(distance,decimals=3)


def ready_check():
    adc = ADS1015()
    GAIN = 1
    READY=0

    measures=[0]*3
    x=0
    counter=0
    for _ in range(30):
        values = [0]*4
        for i in range(4):
            values[i] = adc.read_adc(i, gain=GAIN)

        measures=values[2]
        #x=x+1
        #if x==2:
        #    x=0

        #print("milliVolts")
        #print(measures[0], measures[1])
        #print(np.abs(measures[0]-measures[1]))

        #print("milliVolts")
        #print(measures)

#        if np.abs(measures[0]-measures[1]) <=200 and measures[0] >=1000:
#            #print("System betriebsbereit")
#            READY +=1
#        else:
            #print("System nicht betriebsbereit")
#            READY -=1

        if measures <=1400:
            counter += 1



        time.sleep(0.05)

    #print("counter abs: "+str(counter)+" relative: "+ str(counter/30))
    #GPIO.cleanup()

    if counter <= 5:
        return True
    else:
        return False


    #return READY > 0


#beanheight=bean_height(avg=True)
#print(bean_height(avg=True))
#ready= ready_check()
#for i in range(0,3):
#   print(scan_rfid())
#   time.sleep(2)

#if __name__ == "__main__":
    #print("Test RFID \n")
    #raspi_gpio_init()
    #print(scan_rfid())
    #GPIO.cleanup()
