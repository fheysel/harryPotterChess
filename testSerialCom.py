import re
from nanpy import (ArduinoApi, SerialManager)
from time import sleep

#START WITH ARDUINO SETUP
# set up setial connection
EN = 8
X_DIR_PIN = 5
Y_DIR_PIN = 6
Z_DIR_PIN = 7

X_STP_PIN = 2
Y_STP_PIN = 3
Z_STP_PIN = 4

delayTime = 30 #Delay between each pause (uS)
stps = 6400 # steps in one revolution

try:
    connection = SerialManager()
    duino = ArduinoApi(connection = connection)


except:
    print("Connection to Arduino failed")

 #VOID SETUP
    duino.pinMode(X_DIR_PIN, OUTPUT)
    duino.pinMode(X_STP_PIN, OUTPUT)

    duino.pinMode(Y_DIR_PIN, OUTPUT)
    duino.pinMode(Y_STP_PIN, OUTPUT)

    duino.pinMode(Z_DIR_PIN, OUTPUT)
    duino.pinMode(Z_STP_PIN, OUTPUT)

    duino.pinMode(EN, OUTPUT)
    duino.digitalWrite(EN, LOW)

    for x in range(5):
        step(True, X_DIR_PIN, X_STP_PIN, 6400)

def step(dir, dirPin, stepperPin, steps):
    delayTime = 0.00008

    duino.digitalWrite(dirPin, dir)
    sleep(0.1)

    for x in range(steps):
        duino.digitalWrite(stepperPin, HIGH)
        sleep(delayTime)
        duino.digitalWrite(stepperPin, LOW)
        sleep(delayTime)

