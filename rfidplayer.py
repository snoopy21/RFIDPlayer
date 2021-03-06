"""
based on example_get_uid.py
reads uid an looks for an existing configuration
else it plays RadioBob
"""
import sys
import logging
import RPi.GPIO as GPIO

from pathlib import Path
from pn532 import *

def mplayer(file_to_play):
    if file_to_play.endswith('.m3u') or file_to_play.endswith('.m3u8'):
        mplayer_string = f'loadlist "{file_to_play}"\n'
    else:
        mplayer_string = f'loadfile "{file_to_play}"\n'
    with open('/tmp/mplayer-control', 'w') as mplayer_named_pipe:
        logger.info(f'für named pipe: {mplayer_string}')
        mplayer_named_pipe.write(mplayer_string)

if __name__ == '__main__':
    logger = logging.getLogger('rfidplayer')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('rfidplayer.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    logger.info('startup rfidplayer.py')
    try:
        pn532 = PN532_SPI(debug=False, reset=20, cs=4)

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()
        logger.info('startup sound')
        # Startup Sound
        mplayer('/home/pi/RFIDPlayer/dampflokomotive.mp3')
        logging.info('Waiting for RFID/NFC card...')
        base_path = (Path(__file__).parent / "../nfc_uids")
        nfc_uid_string = ''
        active_uid = ''
        for_counter = 0
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            logging.info('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue
            # UID as String for file lookup
            for i in uid:
                if for_counter == 0:
                    nfc_uid_string += hex(i)
                else:
                    nfc_uid_string += '_' + hex(i)
                for_counter += 1
            logger.info(f'UID-String: {nfc_uid_string}')
            #print('UID-String:', nfc_uid_string)
            # active uid does not need a restart
            if nfc_uid_string != active_uid:
                # try open file
                try:
                    nfc_uid_path = (base_path / nfc_uid_string).resolve()
                    with open(nfc_uid_path) as f:
                        mplayer(f.read().rstrip())
                    f.close()
                    # remember actual uid
                    active_uid = nfc_uid_string
                except IOError as e:
                    #print('IOError', e)
                    logger.error('IOError: %(str(e))s')
                    #mplayer('http://streams.radiobob.de/bob-shlive/mp3-192/mediaplayer/', )
                    mplayer('http://streams.radiobob.de/bob-shlive/mp3-192/mediaplayer/')
                    active_uid = nfc_uid_string
                except:
                    logger.error('Fatal Error %(str(sys.exc_info()[0]))s')
                    mplayer('/home/pi/RFIDPlayer/polizeisirene.mp3')
                    #print('was ging gründlich schief:', sys.exc_info()[0])
            else:
                logging.info('läuft bereits')
            for_counter = 0
            nfc_uid_string = ''
    except Exception as e:
        #print(e)
        logger.error(e)
    finally:
        GPIO.cleanup()
