@echo off
setlocal

title Wave Tec - Instalacao
color 0B

cd /d "%~dp0"
cd ..

set "PROJECT_DIR=%CD%"
set "VENV_DIR=%PROJECT_DIR%\venv"

echo =====================================================
echo             WAVE TEC - INSTALACAO
echo =====================================================
echo.

echo Verificando Python...
where python >nul 2>nul
if errorlevel 1 (
    echo Python nao encontrado no PATH.
    echo Instale o Python 3.11 ou superior e marque a opcao:
    echo "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

python --version

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo.
    echo Criando ambiente virtual...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Erro ao criar o ambiente virtual.
        pause
        exit /b 1
    )
) else (
    echo.
    echo Ambiente virtual ja existe.
)

echo.
echo Ativando ambiente virtual e instalando dependencias...
call "%VENV_DIR%\Scripts\activate.bat"

python -m pip install --upgrade pip
python -m pip install -r "%PROJECT_DIR%\requirements.txt"
if errorlevel 1 (
    echo Erro ao instalar as dependencias.
    pause
    exit /b 1
)

echo.
echo Aplicando migracoes do banco de dados...
python manage.py migrate
if errorlevel 1 (
    echo Erro ao aplicar migracoes.
    pause
    exit /b 1
)

echo.
echo =========================================
echo Sistema instalado com sucesso!

echo.
echo Para iniciar: execute iniciar.bat

echo.
echo Acesse no navegador:

echo http://127.0.0.1:8000

echo =========================================
echo.
pause
endlocal