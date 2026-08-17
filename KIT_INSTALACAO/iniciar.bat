@echo off
setlocal

title Wave Tec v1.0
color 0B

cd /d "%~dp0"
cd ..

set "PROJECT_DIR=%CD%"
set "VENV_DIR=%PROJECT_DIR%\venv"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo.
    echo Ambiente virtual nao encontrado.
    echo Execute primeiro: instalar.bat
    echo.
    pause
    exit /b 1
)

echo ==========================================
echo            WAVE TEC v1.0
echo ==========================================
echo.

call "%VENV_DIR%\Scripts\activate.bat"

echo Abrindo navegador...
start http://127.0.0.1:8000

echo Iniciando servidor Django...
python manage.py runserver

pause
endlocal