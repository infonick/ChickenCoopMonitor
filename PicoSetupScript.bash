#!/bin/bash

RED='\033[0;31m' # Red Text Color
NC='\033[0m' # No Text Color

printf "Updating the system software...\n"
sudo apt update -y
sudo apt upgrade -y

printf "Installing any missing dependencies...\n"
sudo apt install git -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo pip3 install rshell

# Check that user belongs to dialout group for serial communication.
if ! id -nGz "$USER" | grep -qzxF dialout
then
    printf "Adding user '$USER' to the 'dialout' group... ${RED}"
    sudo usermod -aG dialout $USER
	printf "${NC}done.\n"
fi


printf "Copying files to Pi Pico... \n"
cd $HOME/ChickenCoopMonitor/Pico\ Code/
rshell cp -r * /pyboard/
printf "Copying complete. \n"

printf "Resetting the Raspberry Pi Pico... ${RED}"
rshell repl "~ import machine ~ machine.soft_reset()~"
printf "${NC}done.\n"

