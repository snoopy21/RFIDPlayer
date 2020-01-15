#!/usr/bin/python3

# use rotary encoder for volume control

import RPi.GPIO as GPIO
from ky040 import KY040
import os, time
from subprocess import check_call


def rotaryChangeCW():
   check_call("./scripts/playout_controls.sh -c=volumeup", shell=True)

def rotaryChangeCCW():
   check_call("./scripts/playout_controls.sh -c=volumedown", shell=True)

def switchPressed(dummy):
   check_call("./scripts/playout_controls.sh -c=mute", shell=True)


if __name__ == "__main__":

   CLOCKPIN = 16
   DATAPIN = 37
   SWITCHPIN = 18

   GPIO.setmode(GPIO.BCM)

   ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, rotaryChangeCW, rotaryChangeCCW, switchPressed)

   ky040.start()

   try:
      while True:
         time.sleep(0.2)
   finally:
      ky040.stop()
      GPIO.cleanup()