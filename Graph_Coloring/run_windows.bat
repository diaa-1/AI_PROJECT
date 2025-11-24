@echo off
cd /d "C:\Users\W.I\OneDrive\Desktop\AI-Project\Graph_Coloring"

echo Creating virtual environment...
python -m venv .venv

echo Activating environment...
call .venv\Scripts\activate.bat

echo Installing required packages...
pip install --upgrade pip
pip install networkx matplotlib numpy

echo Running demo...
python src\run_demo.py

echo Done.
pause