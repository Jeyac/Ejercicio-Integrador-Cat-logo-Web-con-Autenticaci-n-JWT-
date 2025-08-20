@echo off
echo Iniciando frontend...

cd frontend

REM Instalar dependencias
echo Instalando dependencias...
npm install

REM Iniciar servidor de desarrollo
echo Iniciando servidor de desarrollo...
npm run serve

pause
