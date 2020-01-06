"""
wartet auf Knopfdrücke und übergibt dann entsprechende mplayer befehle
"""

import logging
import RPi.GPIO as GPIO

from gpiozero import Button
from signal import pause

def mplayer(cmd_string):
    with open('/tmp/mplayer-control', 'w') as mplayer_named_pipe:
        logger.info(f'Befehl: {cmd_string}')
        mplayer_named_pipe.write(cmd_string)

def pause_pressed():
    #print('pause')
    mplayer(f'pause\n')

def skip_backward():
    #print('skip_backward')
    mplayer(f'pt_step -1\n')

def skip_forward():
    #print('skip_forward')
    mplayer(f'pt_step 1\n')

def stop():
    #print('stop')
    mplayer(f'stop\n')

if __name__ == '__main__':
    logger = logging.getLogger('button_listener')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('button_listener.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    logger.info('startup button_listener.py')
    
    # Button Zuordnungen
    button_skip_forward = Button(5)
    button_skip_backward = Button(13)
    button_pause = Button(6)
    #button_stop = Button(25)
    
    button_skip_backward.when_pressed = skip_backward
    button_skip_forward.when_pressed = skip_forward
    button_pause.when_pressed = pause_pressed
    #button_stop.when_pressed = stop
    
    pause()
