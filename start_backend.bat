@echo off
echo Iniciando backend...

cd backend

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Crear archivo .env si no existe
if not exist ".env" (
    echo Creando archivo .env...
    copy env.example .env
    echo Generando claves secretas...
    python generate_keys.py
)

REM Inicializar base de datos
echo Inicializando base de datos...
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

REM Iniciar servidor
echo Iniciando servidor Flask...
python wsgi.py

pause
