"""
based on example_get_uid.py
reads uid an looks for an existing configuration
else it plays RadioBob
"""
import RPi.GPIO as GPIO

from pathlib import Path
from pn532 import *


if __name__ == '__main__':
    try:
        pn532 = PN532_SPI(debug=False, reset=20, cs=4)

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        base_path = (Path(__file__).parent / "../nfc_uids")
        nfc_uid_string = ''
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
            # try open file
            try:
                nfc_uid_path = (base_path / nfc_uid_string).resolve()
                #print(nfc_uid_path)
                with open(nfc_uid_path) as f:
                    print(f.read().rstrip())
                f.close()
            except IOError as e:
                print('IOError', e)
            for_counter = 0
            nfc_uid_string = ''
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
