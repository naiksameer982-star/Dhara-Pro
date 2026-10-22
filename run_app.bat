@echo off
title Dhara PRO - Enterprise Agricultural Platform
cd /d "%~dp0"
echo ========================================================
echo   Starting Dhara PRO - Agricultural Decision Support...
echo ========================================================
echo.
python -m streamlit run app.py
pause
