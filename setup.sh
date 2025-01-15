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


# # Add iotLoader.service to the /lib/systemd/system/ folder
# # By default service is not enabled 
# echo Setup the iotLoader.service to run on startup 
# sudo cp iotLoader.service /lib/systemd/system/iotLoader.service
# # sudo systemctl enable iotLoader.service
# # sudo systemctl start iotLoader.service 
# sudo systemctl status iotLoader.service -n50

echo Install fastapi for web services and a ASGI web server
pip install fastapi --break-system-package
pip install "uvicorn[standard]" --break-system-package
pip install python-multipart --break-system-package
export PATH=$PATH:$HOME/.local/bin

# # Add iotWS.service to the /lib/systemd/system/ folder
# # By default service is not enabled 
# echo Setup the iotWS.service to run on startup 
# sudo cp iotWS.service /lib/systemd/system/iotWS.service
# # sudo systemctl enable iotWS.service
# # sudo systemctl start iotWS.service 
# sudo systemctl status iotWS.service -n50

