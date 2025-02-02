#!/usr/bin/env bash

# Before running this file do the following on the raspbery pi
# Add git and your git info
# sudo apt -y install git
# git config --global user.name "iot"
# git config --global user.email ""
# git clone https://github.com/somervda/skylaser.git



# Make sure apt is updated and we have the latest package lists before we start
# Remember to 'sudo chmod u+x setup.sh' to be able to run this script 
# then 'bash setup.sh'

date
echo 1. Updating and Upgrade apt packages 
sudo apt update -y
sudo apt upgrade -y

echo 2. Installing and rationalizing Python Version Names
sudo apt install -y python-is-python3
sudo apt install -y python3-pip
sudo apt install -y python-dev-is-python3

python --version
pip --version

# Install skyfield https://rhodesmill.org/skyfield/
echo 3. Install skyfield
pip install skyfield --break-system-packages

pip install pandas --break-system-packages

export PATH=$PATH:/home/pi/.local/bin

# Install skyfield https://rhodesmill.org/skyfield/
echo 4. Install i2c and IO support



echo 3. Installing OPi.GPIO 
# Install GPIO support for the orange PI 
# see https://pypi.org/project/RPi.GPIO/ and https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/ 
# Note: Use GPIO.setmode(GPIO.SUNXI) to use "PA01" style channel naming
pip install RPi.GPIO --break-system-packages
# Enable i2c hardware
sudo raspi-config nonint do_i2c 0
# Enable serial hardware but not console thru serial
sudo raspi-config nonint do_serial 2

echo 4. Installing python i2c and oled support
# Adafruit version (Circuit python and python)
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/tree/main 
# Use i2cdetect to make sure you see the i2c device on the I2C 1 bus (Pins 3 and 5)  
# i2cdetect -y 1
echo 4a. Install i2c utilities
#  Can run i2c scans i.e. 'i2cdetect -y 1'
sudo apt-get install -y i2c-tools
# Give pi user access to i2c
sudo usermod -a -G spi,gpio,i2c pi
echo 4b. OLED Installing adafruit i2c and oled support
pip3 install adafruit-circuitpython-ssd1306 --break-system-packages

# pca9685 is needed to support the servo kit library
pip3 install adafruit-circuitpython-pca9685 --break-system-packages
#  see https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/using-the-adafruit-library
pip3 install adafruit-circuitpython-servokit  --break-system-packages

# GPS module connect via serial
# see https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
pip install pynmea2 --break-system-packages
# Note: compass uses gy271compass.py library already loaded in project files
# Use gpiozero for managing a rotary control https://gpiozero.readthedocs.io/en/stable/index.html
pip install gpiozero --break-system-packages

sudo pip3 install smbus2 --break-system-packages

# # Add iotLoader.service to the /lib/systemd/system/ folder
# # By default service is not enabled 
# echo Setup the iotLoader.service to run on startup 
# sudo cp iotLoader.service /lib/systemd/system/iotLoader.service
# # sudo systemctl enable iotLoader.service
# # sudo systemctl start iotLoader.service 
# sudo systemctl status iotLoader.service -n50

# echo Install fastapi for web services and a ASGI web server
# pip install fastapi --break-system-package
# pip install "uvicorn[standard]" --break-system-package
# pip install python-multipart --break-system-package
# export PATH=$PATH:$HOME/.local/bin

# # Add iotWS.service to the /lib/systemd/system/ folder
# # By default service is not enabled 
# echo Setup the iotWS.service to run on startup 
# sudo cp iotWS.service /lib/systemd/system/iotWS.service
# # sudo systemctl enable iotWS.service
# # sudo systemctl start iotWS.service 
# sudo systemctl status iotWS.service -n50

