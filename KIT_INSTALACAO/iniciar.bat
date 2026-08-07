@echo off
title Wave Tec v1.0
color 0B

cd /d %~dp0
cd ..

echo ==========================================
echo            WAVE TEC v1.0
echo ==========================================
echo.

call venv\Scripts\activate

echo Iniciando servidor...
start http://127.0.0.1:8000

python manage.py runserver

pause