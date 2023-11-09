#!bin/sh

# update pip
python3 -m pip install --user --upgrade pip

# Make sure venv is installed
python3 -m pip install --user virtualenv

# Create the environment
python3 -m venv ../env-stellar

# Activate the environment
source ../env-stellar/bin/activate

# update pip for the version in the virtual environment
python3 -m pip install --user --upgrade pip

# Installs dependencies from requirements.txt
python3 -m pip install -r requirements.txt
