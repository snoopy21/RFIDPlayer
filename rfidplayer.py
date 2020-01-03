"""
based on example_get_uid.py
reads uid an looks for an existing configuration
else it plays RadioBob
"""
import sys
import RPi.GPIO as GPIO

from pathlib import Path
from pn532 import *

def mplayer(file_to_play):
    if file_to_play.endswith('.m3u') or file_to_play.endswith('.m3u8'):
        mplayer_string = f'loadlist "{file_to_play}"\n'
    else:
        mplayer_string = f'loadfile "{file_to_play}"\n'
    with open('/tmp/mplayer-control', 'w') as mplayer_named_pipe:
        mplayer_named_pipe.write(mplayer_string)

if __name__ == '__main__':
    try:
        pn532 = PN532_SPI(debug=False, reset=20, cs=4)

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        base_path = (Path(__file__).parent / "../nfc_uids")
        nfc_uid_string = ''
        active_uid = ''
        for_counter = 0
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
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
            print('UID-String:', nfc_uid_string)
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
                    print('IOError', e)
                    #mplayer('http://streams.radiobob.de/bob-shlive/mp3-192/mediaplayer/', )
                    mplayer('/home/pi/music/pepe_lienhard-swiss_lady.mp3')
                    active_uid = nfc_uid_string
                except:
                    print('was ging gründlich schief:', sys.exc_info()[0])
            else:
                print('läuft bereits')
            for_counter = 0
            nfc_uid_string = ''
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
