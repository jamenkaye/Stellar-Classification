# Setup Script for the virtual environment

# Make sure pip is up to date
py -m pip install --upgrade pip

# Make sure you have virtualenv - needed to make sure 
pip install virtualenv

# Creates the environment
py -m venv ..\env-stellar

# Activates the environment
.\..\env-stellar\Scripts\activate

# Make sure pip is up to date, but for the copy of pip in env-stellar
py -m pip install --upgrade pip

# Installs dependencies from requirements.txt
py -m pip install -r requirements.txt
