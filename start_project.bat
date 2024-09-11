@echo off
REM Check if the virtual environment exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install required packages if not already installed
echo Installing required packages...
pip install -r requirements.txt

REM Run the Python project
echo Starting the project...
python main.py

REM Deactivate the virtual environment after running the project
deactivate
