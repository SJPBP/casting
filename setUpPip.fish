#!/bin/fish

# Install pip if not installed on Arch
# Source: https://github.com/fish-shell/fish-shell/issues/1774#issuecomment-60508322
if not type -q pip 
	echo -e "Python pip not Installed"
	echo -e "Installing Python pip on Arch Distros"
	sudo pacman -S --needed --noconfirm python-pip 
end


# Get options from argument
set firstArugment $argv[1] 

# Setting name of venv custom directory
# Source: https://stackoverflow.com/a/67639805
set base (status dirname) # output directory where script is located
set customDir "$base/venvDir" 


function createVenvDir
	# Get location of custom directory location
	set customDir $argv[1]

	python3 -m venv "$customDir"  

	echo -e "venv has be created at $customDir" 

	activateVenv

end

function checkIfVenvRunning
	# Source: https://stackoverflow.com/a/15454916, tells how to compare 
	# Source: https://stackoverflow.com/a/53952253, tells to check with \usr
	# 1 means venv is running and 0 means venv is not running
	# real_prefix is avaiable venv 
	set InVenv $( python -c 'import sys; print ("0" if sys.prefix == "/usr" else "1")')

	if [ $InVenv = 1 ]
		echo "yes"
	else if [ $InVenv = 0 ]
		echo "no"
	end
end

function activateVenv
	# Check venv is created
	if ls $customDir 2&>/dev/null

		# Check venv not already running
		if [ (checkIfVenvRunning) = "no" ]
			source "$customDir/bin/activate.fish"
			echo -e "Activated venv"
		end
	else
		echo -e "VenvDir Not Found"
	end
end

function outputOption
	set option $argv[1]
	set message $argv[2]

	echo -e "\t$option\t$message"
end


switch $firstArugment
case "-h" "--help"
	echo -e "SetUpVenv, version 1.0.0"
	echo -e "Setup Python Virtual Enviroment to custom directory."
	echo -e "Usage:\t./setVenv.py [option] [argument]"
	echo -e "SetUpVenv options:"

	outputOption "-h, --help" "give this help list" 

	# echo -e "\t\t-d\t\tTakes custom directory as argument and setup Virtual Enviroment"
	outputOption "-a" "\tActive Virtual Enviroment"
	outputOption "-d" "\tDeactive Virtual Enviroment"
	outputOption "-c" "\tCheck if running Virtual Enviroment"

	outputOption "-s" "\tCreate venvDir and activate venv"

	outputOption "-b" "\tBackup the installed python packages to requirements.txt"
	outputOption "it" "\tInstall packages from requirements.txt"
	outputOption "-u" "\tUpdate all pip modules using pip-review"

case "-s"
	# Create venv in venvDir directory
	createVenvDir $customDir	

	# Active the venv
	activateVenv

case "-b"
	activateVenv

	# Save install modules in venv to requirements.txt
	pip freeze > requirements.txt

case "-i"
	activateVenv

	# Install from requirements.txt
	pip install -r requirements.txt

case "-u"
	activateVenv

	pip install pip-review	# Module to update all modules at same time

	# Upgrade the packages interactively
	pip-review --local --interactive

	# Upgrade automatically
	pip-review --local --auto

case "-a"
	activateVenv

case "-c"
	if [ (checkIfVenvRunning) = "yes" ]
		echo "Python virtual enviroment is running"
	else
		echo "Python virtual enviroment is not running"
	end

case "-d"
	# Deactivate if venv is running
	if [ (checkIfVenvRunning) = "yes" ]
		deactivate
	end
end
