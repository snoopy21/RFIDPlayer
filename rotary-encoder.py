#!/usr/bin/python3

# use rotary encoder for volume control

import RPi.GPIO as GPIO
from ky040 import KY040
import os, time
from subprocess import check_call


def rotaryChangeCW():
   print("volumeup")
   check_call("/usr/bin/amixer -M set PCM 5%+", shell=True)

def rotaryChangeCCW():
   print('volumedown')
   check_call("/usr/bin/amixer -M set PCM 5%-", shell=True)

def switchPressed(dummy):
   print("mute")
   check_call("/usr/bin/amixer set PCM toggle", shell=True)


if __name__ == "__main__":

   CLOCKPIN = 23
   DATAPIN = 22
   SWITCHPIN = 24

   GPIO.setmode(GPIO.BCM)

   ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, rotaryChangeCW, rotaryChangeCCW, switchPressed)

   ky040.start()

   try:
      while True:
         time.sleep(0.2)
   finally:
      ky040.stop()
      GPIO.cleanup()