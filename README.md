# RFIDPlayer
Raspberrypi-Musik-Player with RFID support

## Teileliste
- Raspberry Pi 3B
- PN532 NFC HAT (https://www.waveshare.com/wiki/PN532_NFC_HAT)
- Logitech S150 USB-Lautsprecherboxen
- 5 Knöpfe (z.B. Arcade Button mit Mikroschalter bei Conrad)
- Kabelset (z.B. Kabelset Raspberry PI, 20 x1 Stück 50 cm bei Conrad)
- Kodierter Drehschalter

## Software
- Raspbian
- mplayer

## Installation

### Shutdown/Startup per Knopf
- Knopf mit Pin 5 (SCL bzw. GPIO3) und Pin 6 (GND) verbinden
- /boot/config.txt editieren und ```dtoverlay=gpio-shutdown,gpio_pin=3``` hinzufügen

### weitere Knöpfe/Drehschalter
- Pause PIN 31 (GPIO6) und PIN 39 (GND)
- Skip backward PIN 33 (GPIO13) und PIN 34 (GND)
- Skip forward PIN 29 (GPIO5) und PIN 30 (GND)
- Drehschalter CLK -> PIN 16 (GPIO 23), DT -> PIN 15 (GPIO 22), SW -> PIN 18 (GPIO 24), + -> PIN 4 (5V), GND -> PIN 25 (GND)

### NFS-Share mounten beim Start
sudo mkdir /mnt/glenelg_music
sudo vi /etc/fstab -> 

### /etc/rc.local anpassen
mit ```sudo vi /etc/rc.local``` editieren
```
# Create named pipe for mplayer
mkfifo /tmp/mplayer-control
chmod 666 /tmp/mplayer-control
```

### .bashrc anpassen
in die .bashrc des users pi, auto login aktivieren nicht vergessen, folgendes einfügen:
```
# Start mplayer in slave mode
mplayer -slave -input file=/tmp/mplayer-control -idle &

# Start Python RFID-reader-mplayer-control script
python3 /home/pi/RFIDPlayer/rfidplayer.py &

# Start des Button-Listener scripts
python3 /home/pi/RFIDPlayer/button_listener.py &
```

### RFIDPlayer Software installieren
git clone https://github.com/snoopy21/RFIDPlayer.git

### NFC Hat
Beispielcodes:
wget https://www.waveshare.com/w/upload/6/67/Pn532-nfc-hat-code.7z
allenfalls folgende Liberaries installieren
sudo apt-get install python3-rpi.gpio
sudo apt install python3-gpiozero (nur falls Raspbian Lite verwendet wird)
sudo apt-get install python3-pip
sudo pip3 install spidev
sudo pip3 install serial

Jumper-Settings -> Dokumentation https://www.waveshare.com/wiki/PN532_NFC_HAT

### Einstellungen Audio
install pulseaudio
aplay -l
interne Soundkarte abschalten -> sudo vi /usr/share/alsa/alsa.conf
sudo cp /lib/systemd/system/triggerhappy.service /etc/systemd/system

Triggerhappy -> Berechtigung... (chown pi audio.conf)
/etc/triggerhappy/triggers.d/audio.conf:
```
KEY_VOLUMEUP 1  /usr/bin/amixer -M set PCM 5%+

KEY_VOLUMEUP 2  /usr/bin/amixer -M set PCM 5%+

KEY_VOLUMEDOWN 1  /usr/bin/amixer -M set PCM 5%- 

KEY_VOLUMEDOWN 2  /usr/bin/amixer -M set PCM 5%- 

KEY_MUTE 1 /usr/bin/amixer set PCM toggle
```

### Services installieren
sudo cp rotary-encoder.service /etc/systemd/system/rotary-encoder.service
sudo systemctl enable rotary-encoder.service
sudo chmod +x rotary-encoder.py

# inspiriert von
- https://www.instructables.com/id/Raspberry-Pi-based-RFID-Music-Robot/
- https://www.heise.de/select/ct/2017/17/1502995683647692
- http://www.akeric.com/blog/?p=1976
- https://www.stderr.nl/Blog/Hardware/RaspberryPi/PowerButton.html
- https://www.raspberrypi.org/documentation/usage/gpio/ bzw. https://gpiozero.readthedocs.io/en/stable/recipes.html#button
