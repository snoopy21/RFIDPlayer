"""
wartet auf Knopfdrücke und übergibt dann entsprechende mplayer befehle
"""

import logging
import RPi.GPIO as GPIO

from gpiozero import Button

if __name__ == '__main__':
    logger = logging.getLogger('button_listener')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('button_listener.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    logger.info('startup button_listener.py')
    try:
        
    except Exception as e:
        logger.error(e)
    finally:
        GPIO.cleanup()
