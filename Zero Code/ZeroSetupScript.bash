#!/bin/bash

# -------------------------------------------------------------
# Two functions borrowed from raspi-config
# -------------------------------------------------------------
get_config_var() {
  lua - "$1" "$2" <<EOF
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
local found=false
for line in file:lines() do
  local val = line:match("^%s*"..key.."=(.*)$")
  if (val ~= nil) then
    print(val)
    found=true
    break
  end
end
if not found then
   print(0)
end
EOF
}

set_config_var() {
  lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=true
  end
  print(line)
end

if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}

# Allows the set_config_var function to be passed to a sudo session for execution
set_config_var_declared=$(declare -f set_config_var)

# -------------------------------------------------------------
# Begin Script
# -------------------------------------------------------------
RED='\033[0;31m' # Red Text Color
NC='\033[0m' # No Text Color
echo This script installs the Chicken Coop Monitor on a Raspberry Pi Zero W. It is not tested with any other Raspberry Pi version.
printf "${RED}The script makes extensive use of the \'sudo\' command in order to complete the installation and many changes will be made to your system.${NC}\n"
echo "----------------------"
echo "Do you wish to proceed with the installation? (y/n) "
read ans
if [ "$ans" != "y"  -a  "$ans" != "Y"  -a  "$ans" != "yes"  -a  "$ans" != "YES" ]
then
  echo "Exiting.."
  exit
fi


echo "Updating the system software..."
sudo apt update -y
sudo apt upgrade -y

echo "Installing any missing dependencies"
sudo apt install git -y
sudo apt install apache2 -y
sudo apt install php7.3 libapache2-mod-php -y
sudo apt install sqlite3 -y
sudo apt install php7.3-sqlite
sudo apt install python3 -y
sudo apt install python-picamera python3-picamera -y
sudo apt install python-gpiozero python3-gpiozero -y
sudo apt install python-serial python3-serial -y #not sure what the correct one is for pyserial


# Create the database folder if required
if [ ! -d /var/database ]
then 
  echo "Creating database folder at /var/database"
  sudo mkdir /var/database
fi


# Check that user belongs to www-data group. Borrowed from https://stackoverflow.com/a/46651233
if ! id -nGz "$USER" | grep -qzxF www-data
then
    echo "Adding user '$USER' to the 'www-data' group."
    sudo usermod -aG www-data $USER
fi



# Copy database and website files
printf "Copy and overwrite website files in /var/www/html/? (y/n) "
read ans
if [ "$ans" == "y"  -o  "$ans" == "Y"  -o  "$ans" == "yes"  -o  "$ans" == "YES" ]
then
  printf "\nCopying website files...  "
  rm -r /var/www/html/*
  sudo cp -r Website\ Code/* /var/www/html/
  printf "done.\n"
else
  printf " ... skipped.\n"
fi

printf "Copy and overwrite database in /var/database/? (y/n) "
read ans
if [ "$ans" == "y"  -o  "$ans" == "Y"  -o  "$ans" == "yes"  -o  "$ans" == "YES" ]
then
  printf "\nCopying database file...  "
  sudo cp database/CCMonitor.db /var/database/CCMonitor.db
  printf "done.\n"
else
  printf " ... skipped.\n"
fi


# Refresh folder permissions, as per https://itectec.com/ubuntu/ubuntu-permissions-problems-with-var-www-html-and-the-own-home-directory-for-a-website-document-root/
echo "Setting permissions for /var/database"
sudo chgrp -R www-data /var/database
sudo find /var/database -type d -exec chmod g+rwx {} +
sudo find /var/database -type f -exec chmod g+rw {} +

sudo chown -R $USER /var/database
sudo find /var/database -type d -exec chmod u+rwx {} +
sudo find /var/database -type f -exec chmod u+rw {} +

sudo find /var/database -type d -exec chmod g+s {} +

echo "Setting permissions for /var/www/html"
sudo chgrp -R www-data /var/www/html
sudo find /var/www/html -type d -exec chmod g+rx {} +
sudo find /var/www/html -type f -exec chmod g+r {} +

sudo chown -R $USER /var/www/html
sudo find /var/www/html -type d -exec chmod u+rwx {} +
sudo find /var/www/html -type f -exec chmod u+rw {} +

sudo find /var/www/html -type d -exec chmod g+s {} +


# Remove permissions for 'other' users
echo "Removing extraneous permissions for 'other' users in /var/www/html/ and /var/database/."
sudo chmod -R o-rwx /var/www/html/
sudo chmod -R o-rwx /var/database/


# Setup cron autostart for business logic and webcam python scripts
printf "Set up cron to automatically start python files for Pi Camera and Business Logic? (y/n) "
read ans
if [ "$ans" == "y"  -o  "$ans" == "Y"  -o  "$ans" == "yes"  -o  "$ans" == "YES" ]
then
  filename="crontab_backup_$(date +'%s').txt"
  crontab -l > $filename #create backup of existing crontab configuration
  printf "\n"
  echo "Backup of cron configuration saved to $filename ."
  printf "Setting up crontab with new jobs...  "
  crontab -l > crontab_new.txt
  echo "@reboot python3 $HOME/ChickenCoopMonitor/Zero\ Code/Business\ Logic/Pi\ Zero\ Bsiness\ Logic.py" >> crontab_new.txt
  echo "@reboot python3 $HOME/ChickenCoopMonitor/Zero\ Code/Business\ Logic/picam.py" >> crontab_new.txt
  crontab crontab_new.txt
  rm crontab_new.txt
  printf "done.\n"
else
  printf " ... skipped.\n"
fi



# -------------------------------------------------------------
# Edit Raspberry Pi /boot/config.txt file
# -------------------------------------------------------------
RPI_CFG_FILE='/boot/config.txt'

#Enable Raspberry Pi Camera on CSI ribbon
#start_x=1             # enable camera
#gpu_mem=128           # camera required 128mb minimum
#disable_camera_led=1  # optional, if you don't want the camera led to glow
CAMERA_LED_SETTING=0
CUR_GPU_MEM=$(get_config_var gpu_mem $RPI_CFG_FILE)

printf "Enabling Raspberry Pi Camera on CSI ribbon...  "
sudo bash -c "$set_config_var_declared; set_config_var start_x 1 $RPI_CFG_FILE"
if [ -z "$CUR_GPU_MEM" ] || [ "$CUR_GPU_MEM" -lt 128 ]
then
  sudo bash -c "$set_config_var_declared; set_config_var gpu_mem 128 $RPI_CFG_FILE"
fi
printf "done.\n"

echo "Disable Pi Camera LED? (y/n) "
read ans
if [ "$ans" == "y"  -o  "$ans" == "Y"  -o  "$ans" == "yes"  -o  "$ans" == "YES" ]
then
  CAMERA_LED_SETTING=1
fi
sudo bash -c "$set_config_var_declared; set_config_var disable_camera_led $CAMERA_LED_SETTING $RPI_CFG_FILE"



# Set up UART with PL011 for best reliability - requires disabling bluetooth.
# dtoverlay=disable-bt             # Disables bluetooth in config.txt
# enable_uart=1                    # Enables uart communication
# sudo systemctl disable hciuart   # Also required to disable bluetooth and set up UART.
printf "Setting up UART with PL011 for best reliability (NOTE: this requires disabling bluetooth)... "
if ! grep "dtoverlay=disable-bt" $RPI_CFG_FILE
then
  sudo echo "dtoverlay=disable-bt" >> $RPI_CFG_FILE
fi

sudo bash -c "$set_config_var_declared; set_config_var enable_uart 1 $RPI_CFG_FILE"

sudo systemctl disable hciuart
printf "done.\n"


# -------------------------------------------------------------
# -------------------------------------------------------------
echo "*************************************************"
echo "Setup script is complete. Please note: it is recommended that you enable SSH for headless installations."

echo "Reboot now to complete installation? (y/n) "
read ans
if [ "$ans" == "y"  -o  "$ans" == "Y"  -o  "$ans" == "yes"  -o  "$ans" == "YES" ]
then
  sudo reboot
fi

exit
