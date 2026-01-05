#!/bin/bash

# Install pip
echo -e "Installing Python pip on Arch Distros"
sudo pacman -S --needed --noconfirm python-pip | echo "Failed to install Python pip" 

# Setting how to behave to Different first argument
firstArugment=$1

case $firstArugment in

	"-h" | "--help")
		echo -e "SetUpVenv, version 1.0.0"
		echo -e "Setup Python Virtual Enviroment to custom directory."
		echo -e "Usage:\t./setVenv.py [option] [argument]"
		echo -e "SetUpVenv options:"
		echo -e "\t\t-h, --help\t\t\tgive this help list"
		echo -e "\t\t-d\t\t\t\tTakes custom directory as argument"
		;;
	"-d")
		customDir=$2

		python3 -m venv $customDir && echo -e "venv has be created" | exit -2
		
		source "$customDir/bin/active"

		echo -e "Activated venv"

		# Updating pip in venv 
		echo -e "Updating pip to lastest version"
		pip install --upgrade pip | echo "Failed to update pip" && exit -2
esac


