# Catálogo de Productos - Aplicación Full-Stack

Una aplicación web completa para la gestión de un catálogo de productos, construida con **Flask** (backend) y **Vue.js** (frontend), siguiendo los principios de **Clean Architecture**.

> **Documentación Específica:**
> - [Backend Flask](./backend/README.md) - Documentación técnica del backend
> - [Frontend Vue.js](./frontend/README.md) - Documentación técnica del frontend

## Características Principales

### 🌐 Acceso Multiplataforma
- **Desarrollo local**: Acceso desde `localhost`
- **Red local**: Acceso desde cualquier dispositivo en la misma red WiFi
- **Configuración automática** de CORS para acceso desde red local
- **Health check endpoints** para verificar el estado del servidor

### Autenticación JWT
- **Login/Registro** de usuarios
- **Tokens de acceso y refresh**
- **Rutas protegidas** en backend y frontend
- **Manejo automático** de sesiones expiradas
- **Formulario de login moderno** con validación y efectos visuales

### Gestión de Entidades
- **Categorías**: Clasificación de productos
- **Presentaciones**: Formatos de presentación
- **Productos**: Gestión completa con precios y estado
- **Tarjetas interactivas** que funcionan como botones cuando el usuario está autenticado

### Interfaz Moderna
- **Bootstrap 5** para diseño responsive
- **Vue.js 3** con Composition API
- **Pinia** para manejo de estado
- **Animaciones** y transiciones suaves
- **Diseño mejorado** con botones grandes y tarjetas interactivas
- **Formulario de login moderno** con efectos visuales
- **Navegación intuitiva** con botones posicionados estratégicamente

### Arquitectura Sólida
- **Clean Architecture** en el backend
- **SQLAlchemy** con PostgreSQL
- **Migrations** con Alembic
- **Validación** con Marshmallow

## 📋 Requisitos Previos

### Backend (Python 3.13+)
- Python 3.13 o superior
- PostgreSQL 12+
- pip (gestor de paquetes Python)

### Frontend (Node.js)
- Node.js 16+ 
- npm 8+ o yarn

## Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Jeyac/Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-.git
cd Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-
```

### 2. Configurar Variables de Entorno

**Backend** - Crear `backend/.env`:
```env
# Configuración de la base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=catalogo_db
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password_postgres

# Claves secretas (generar claves seguras)
# Ejemplos de claves generadas (cambiar por las tuyas):
SECRET_KEY=mi_clave_secreta_super_segura_2024_xyz123
JWT_SECRET_KEY=mi_jwt_secret_key_super_segura_2024_abc456

# Configuración de Flask
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

**Frontend** - Crear `frontend/.env`:
```env
# URL del backend Flask (para desarrollo local)
VUE_APP_API_URL=http://localhost:5000/api

# Para acceso desde otros dispositivos en la red:
# VUE_APP_API_URL=http://TU_IP_LOCAL:5000/api
# Ejemplo: VUE_APP_API_URL=http://192.168.1.100:5000/api

# Configuración de la aplicación
VUE_APP_TITLE=Catálogo de Productos
VUE_APP_DESCRIPTION=Sistema de administración de productos

# Configuración de desarrollo
NODE_ENV=development
```

### 3. Configurar Base de Datos PostgreSQL
```sql
CREATE DATABASE catalogo_db;
CREATE USER tu_usuario_postgres WITH PASSWORD 'tu_password_postgres';
GRANT ALL PRIVILEGES ON DATABASE catalogo_db TO tu_usuario_postgres;
```

### 4. Instalar y Ejecutar Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python wsgi.py
```

### 5. Instalar y Ejecutar Frontend
```bash
cd frontend
npm install
npm run serve
```

## Acceso a la Aplicación

### Desarrollo Local
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000/api
- **Backend Health Check**: http://localhost:5000/api/health

### Acceso desde Red Local
- **Frontend**: http://TU_IP_LOCAL:8080
- **Backend API**: http://TU_IP_LOCAL:5000/api
- **Backend Health Check**: http://TU_IP_LOCAL:5000/api/health
- **Backend Root**: http://TU_IP_LOCAL:5000

**Ejemplo:**
- **Frontend**: http://192.168.1.100:8080
- **Backend API**: http://192.168.1.100:5000/api

## Estructura del Proyecto

```
catalogo-productos/
├── backend/                    # Backend Flask
│   ├── app/
│   │   ├── domain/            # Entidades de dominio
│   │   ├── application/       # Casos de uso
│   │   ├── infrastructure/    # Repositorios, DB, JWT
│   │   └── interface/         # Blueprints, DTOs
│   ├── migrations/            # Migraciones de base de datos
│   ├── requirements.txt       # Dependencias Python
│   ├── config.py             # Configuración
│   └── wsgi.py               # Punto de entrada
├── frontend/                  # Frontend Vue.js
│   ├── src/
│   │   ├── components/        # Componentes reutilizables
│   │   ├── views/            # Páginas principales
│   │   ├── store/            # Estado con Pinia
│   │   ├── api/              # Cliente HTTP
│   │   └── router/           # Configuración de rutas
│   ├── package.json          # Dependencias Node.js
│   └── vue.config.js         # Configuración Vue CLI
└── README.md                 # Este archivo
```

## API Endpoints

### Autenticación
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login de usuario
- `POST /api/auth/refresh` - Refresh de token
- `GET /api/auth/me` - Información del usuario

### Categorías
- `GET /api/categorias` - Listar categorías (con paginación y búsqueda por nombre)
- `POST /api/categorias` - Crear categoría
- `PUT /api/categorias/:id` - Actualizar categoría
- `DELETE /api/categorias/:id` - Eliminar categoría

### Presentaciones
- `GET /api/presentaciones` - Listar presentaciones (con paginación y búsqueda por nombre)
- `POST /api/presentaciones` - Crear presentación
- `PUT /api/presentaciones/:id` - Actualizar presentación
- `DELETE /api/presentaciones/:id` - Eliminar presentación

### Productos
- `GET /api/productos` - Listar productos (con filtros, paginación y búsqueda por nomnbre)
- `POST /api/productos` - Crear producto
- `PUT /api/productos/:id` - Actualizar producto
- `DELETE /api/productos/:id` - Eliminar producto

## Scripts de Desarrollo

### Backend
```bash
cd backend
# Ejecutar en modo desarrollo
python wsgi.py

# Ejecutar tests
pytest

# Crear migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade
```

### Frontend
```bash
cd frontend
# Servidor de desarrollo
npm run serve

# Construir para producción
npm run build

# Linting
npm run lint
```

### Scripts Automatizados
```bash
# Ejecutar backend (Windows)
start_backend.bat

# Ejecutar frontend (Windows)
start_frontend.bat
```

## Solución de Problemas

### Error de Conexión a Base de Datos
1. Verificar que PostgreSQL esté ejecutándose
2. Confirmar credenciales en `backend/.env`
3. Verificar que la base de datos existe
4. Comprobar permisos del usuario

### Error de CORS
1. Verificar configuración en `backend/config.py`
2. Confirmar que el frontend esté en el puerto correcto
3. Revisar headers de las peticiones
4. Verificar que ambos servicios estén ejecutándose

### Error de Conexión desde Otros Dispositivos
1. **Verificar IP de red**: Usar `ipconfig` (Windows) o `ifconfig` (Linux/Mac) para obtener tu IP real
2. **Configurar CORS**: Agregar tu IP a `CORS_ORIGINS` en `backend/config.py`
3. **Configurar firewall**: Permitir conexiones en puertos 5000 y 8080
4. **Verificar red**: Asegurar que ambos dispositivos estén en la misma red WiFi
5. **Actualizar .env**: Cambiar `VUE_APP_API_URL` a tu IP de red (ejemplo: `http://192.168.1.100:5000/api`)

### Error de PowerShell (Windows)
Si tienes problemas con comandos en PowerShell:
```powershell
# En lugar de: cd .. && python backend/wsgi.py
# Usar:
cd ..
python backend/wsgi.py
```

### Error de JWT
1. Verificar que las claves secretas estén configuradas en `backend/.env`
2. Confirmar que los tokens no hayan expirado
3. Revisar la configuración de CORS
4. Comprobar que el backend esté ejecutándose

### Error de PowerShell (Windows)
Si tienes problemas con comandos en PowerShell:
```powershell
# En lugar de: cd .. && python backend/wsgi.py
# Usar:
cd ..
python backend/wsgi.py
```

## Tecnologías Utilizadas

### Backend
- **Flask 3.0** - Framework web
- **SQLAlchemy 2.0** - ORM
- **PostgreSQL** - Base de datos
- **JWT** - Autenticación
- **Marshmallow** - Validación
- **Alembic** - Migraciones
- **psycopg[binary]** - Driver PostgreSQL

### Frontend
- **Vue.js 3** - Framework frontend
- **Bootstrap 5** - CSS framework
- **Pinia** - Estado global
- **Vue Router 4** - Navegación
- **Axios** - Cliente HTTP
- **Bootstrap Icons** - Iconografía

### Herramientas de Desarrollo
- **Vue CLI** - Herramientas de desarrollo
- **ESLint** - Linting de código
- **Git** - Control de versiones

## Seguridad

### Variables de Entorno
- **Nunca compartas** tus archivos `.env` con credenciales reales
- **Usa ejemplos genéricos** para credenciales de base de datos
- **Genera claves seguras** para `SECRET_KEY` y `JWT_SECRET_KEY`
- **Cambia las credenciales** por defecto de PostgreSQL

### Cómo Generar Claves Seguras
```bash
# Opción 1: Usando Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Opción 2: Usando OpenSSL
openssl rand -base64 32

# Opción 3: Usando Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"

# Opción 4: Generador online (solo para desarrollo)
# https://generate-secret.vercel.app/32
```

### Configuración de Red
- **Tu IP será diferente** a la mostrada en los ejemplos
- **Usa `ipconfig` (Windows) o `ifconfig` (Linux/Mac)** para obtener tu IP real
- **Configura CORS** específicamente para tu red local
- **Considera el firewall** de tu sistema operativo

### Ejemplo de Configuración Segura
```env
# CORRECTO - Usar valores genéricos para credenciales de BD
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password_postgres

# CORRECTO - Usar ejemplos de claves generadas
SECRET_KEY=mi_clave_secreta_super_segura_2024_xyz123
JWT_SECRET_KEY=mi_jwt_secret_key_super_segura_2024_abc456

## Autor

**Jeraldyn** - [GitHub](https://github.com/Jeyac)

## Repositorio

**URL del Repositorio**: https://github.com/Jeyac/Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-.git

## Documentación Adicional

Para información más detallada sobre cada parte del proyecto:

- **[Backend Flask](./backend/README.md)** - Documentación técnica completa del backend
- **[Frontend Vue.js](./frontend/README.md)** - Documentación técnica completa del frontend

---

⭐ Si este proyecto te ha sido útil, ¡dale una estrella!
