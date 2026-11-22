
@echo off
title CLINIQ Smart Clinic
cd /d "%~dp0"

echo ======================================
echo       CLINIQ SMART CLINIC
echo ======================================

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Installation failed. Check your Python setup.
    pause
    exit /b 1
)

echo.
echo Starting CLINIQ...
python -m streamlit run app.py

pause
