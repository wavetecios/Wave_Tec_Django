@echo off
title Backup Wave Tec
color 0E

cd /d %~dp0
cd ..

if not exist BACKUP mkdir BACKUP

echo.
echo Realizando backup...

copy db.sqlite3 BACKUP\db.sqlite3

echo.
echo ==========================================
echo Backup realizado com sucesso!
echo Arquivo salvo em:
echo BACKUP\db.sqlite3
echo ==========================================

pause