@echo off
REM Publica este repositorio en GitHub (Windows).
REM Uso:  publicar.bat https://github.com/TU_USUARIO/condensador-mariposa-loop.git
REM Antes crea el repositorio VACIO en https://github.com/new (sin README ni licencia).
if "%~1"=="" (echo Uso: publicar.bat URL_DEL_REPOSITORIO & exit /b 1)
cd /d "%~dp0"
git remote remove origin 2>nul
git remote add origin %1
git push -u origin main || exit /b 1
git push origin --tags
echo Publicado en %1
