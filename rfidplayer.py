"""
based on example_get_uid.py
reads uid an looks for an existing configuration
else it plays RadioBob
"""

import RPi.GPIO as GPIO

from pn532 import *


if __name__ == '__main__':
    try:
        pn532 = PN532_SPI(debug=False, reset=20, cs=4)

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
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
            for_counter = 0
            nfc_uid_string = ''
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
