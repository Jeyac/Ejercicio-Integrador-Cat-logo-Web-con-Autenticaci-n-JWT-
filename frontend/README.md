# 🎨 Frontend Vue.js - Catálogo de Productos

Frontend de la aplicación de catálogo de productos construido con **Vue.js 3**, **Bootstrap 5** y **Pinia** para el manejo de estado.

## 🏗️ Arquitectura

El frontend está estructurado siguiendo las mejores prácticas de Vue.js:

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── Navbar.vue      # Barra de navegación
│   │   ├── CrudTable.vue   # Tabla genérica para CRUD
│   │   └── CrudForm.vue    # Formulario genérico para CRUD
│   ├── views/              # Páginas principales
│   │   ├── HomeView.vue    # Página de inicio
│   │   ├── LoginView.vue   # Página de autenticación
│   │   ├── CategoriaView.vue    # CRUD de categorías
│   │   ├── PresentacionView.vue # CRUD de presentaciones
│   │   └── ProductoView.vue     # CRUD de productos
│   ├── api/                # Cliente HTTP y endpoints
│   │   ├── http.js         # Configuración de Axios
│   │   ├── auth.js         # Endpoints de autenticación
│   │   ├── categorias.js   # Endpoints de categorías
│   │   ├── presentaciones.js # Endpoints de presentaciones
│   │   └── productos.js    # Endpoints de productos
│   ├── store/              # Estado global con Pinia
│   │   └── auth.js         # Store de autenticación
│   ├── router/             # Configuración de rutas
│   │   └── index.js        # Definición de rutas y guards
│   ├── App.vue             # Componente raíz
│   └── main.js             # Punto de entrada
├── public/                 # Archivos estáticos
├── package.json           # Dependencias Node.js
└── vue.config.js         # Configuración de Vue CLI
```

## 🚀 Características

### 🎨 Interfaz Moderna
- **Bootstrap 5** para diseño responsive
- **Vue.js 3** con Composition API
- **Bootstrap Icons** para iconografía
- **Animaciones** y transiciones suaves
- **Diseño** moderno y profesional

### 🔐 Autenticación
- **Login/Registro** de usuarios
- **Manejo automático** de tokens JWT
- **Guards de ruta** para protección
- **Cerrar sesión** con limpieza de estado

### 📊 Gestión de Datos
- **CRUD completo** para todas las entidades
- **Tablas** con paginación y búsqueda
- **Formularios** con validación
- **Modales** para crear/editar
- **Confirmación** para eliminar

### 🔍 Funcionalidades Avanzadas
- **Búsqueda** en tiempo real
- **Filtros** por categoría y presentación
- **Paginación** configurable
- **Estados de carga** con spinners
- **Notificaciones** de éxito/error

## 📋 Requisitos Previos

- **Node.js 16+**
- **npm 8+** o **yarn**
- **Backend Flask** ejecutándose en `http://localhost:5000`

## 🛠️ Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Jeyac/Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-.git
cd Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-/frontend
```

### 2. Instalar Dependencias
```bash
npm install
# o
yarn install
```

### 3. Configurar Variables de Entorno
Crear archivo `.env` en el directorio `frontend/`:

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

### 4. Ejecutar en Modo Desarrollo
```bash
npm run serve
# o
yarn serve
```

La aplicación estará disponible en: **http://localhost:8080**

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `VUE_APP_API_URL` | URL del backend Flask | `http://localhost:5000/api` |
| `VUE_APP_TITLE` | Título de la aplicación | `Catálogo de Productos` |
| `NODE_ENV` | Entorno de ejecución | `development` |

### Configuración de Vue CLI
El archivo `vue.config.js` contiene la configuración específica:
- **Proxy** para desarrollo
- **Configuración** de build
- **Opciones** de desarrollo

## 🎯 Componentes Principales

### Navbar.vue
Barra de navegación principal con:
- **Logo** y enlaces de navegación
- **Menú desplegable** "Administrar" (cuando está autenticado)
- **Información del usuario** y botón de logout
- **Enlace al login** (cuando no está autenticado)

### CrudTable.vue
Componente genérico para tablas CRUD:
- **Paginación** automática
- **Búsqueda** en tiempo real
- **Acciones** de editar/eliminar
- **Estados de carga**
- **Mensajes** cuando no hay datos

### CrudForm.vue
Componente genérico para formularios:
- **Validación** de campos
- **Manejo** de errores
- **Estados de carga**
- **Botones** de acción

## 🔐 Autenticación

### Flujo de Autenticación
1. **Login**: Usuario ingresa credenciales
2. **Tokens**: Se almacenan access y refresh tokens
3. **Interceptores**: Axios inyecta automáticamente el token
4. **Refresh**: Se renueva automáticamente cuando expira
5. **Logout**: Se limpian todos los tokens

### Store de Autenticación (Pinia)
```javascript
// Estado
- isAuthenticated: boolean
- currentUser: object
- accessToken: string
- refreshToken: string

// Acciones
- login(credentials)
- logout()
- refreshToken()
- initializeAuth()
- ensureAuthenticated()
```

## 🛣️ Rutas y Navegación

### Rutas Públicas
- `/` - Página de inicio
- `/login` - Página de autenticación

### Rutas Protegidas
- `/categorias` - CRUD de categorías
- `/presentaciones` - CRUD de presentaciones
- `/productos` - CRUD de productos

### Guards de Autenticación
- **Verificación** automática de tokens
- **Redirección** al login si no está autenticado
- **Prevención** de acceso a login si ya está autenticado

## 📡 Comunicación con Backend

### Cliente HTTP (Axios)
```javascript
// Configuración base
baseURL: process.env.VUE_APP_API_URL || 'http://localhost:5000/api'
timeout: 10000

// Interceptores
- Request: Inyección automática de token
- Response: Manejo de errores 401

// Variables de entorno
VUE_APP_API_URL=http://localhost:5000/api          // Desarrollo local
VUE_APP_API_URL=http://TU_IP_LOCAL:5000/api        // Red local
// Ejemplo: VUE_APP_API_URL=http://192.168.1.100:5000/api
```

### Endpoints Utilizados
- **Autenticación**: `/auth/*`
- **Categorías**: `/categorias`
- **Presentaciones**: `/presentaciones`
- **Productos**: `/productos`

## 🎨 Estilos y Diseño

### Bootstrap 5
- **Sistema de grid** responsive
- **Componentes** predefinidos
- **Utilidades** CSS
- **Temas** personalizables

### Bootstrap Icons
- **Iconografía** consistente
- **Iconos** para todas las acciones
- **Integración** nativa con Bootstrap

### CSS Personalizado
- **Variables** CSS para colores
- **Animaciones** y transiciones
- **Estilos** específicos de componentes

## 🚀 Scripts de Desarrollo

### Servidor de Desarrollo
```bash
npm run serve
```

### Construir para Producción
```bash
npm run build
```

### Linting
```bash
npm run lint
```

### Linting con Corrección Automática
```bash
npm run lint -- --fix
```

## 🐛 Solución de Problemas

### Error de Conexión al Backend
1. Verificar que el backend esté ejecutándose
2. Confirmar la URL en `VUE_APP_API_URL`
3. Revisar la configuración de CORS
4. Comprobar la conectividad de red

### Error de Conexión desde Otros Dispositivos
1. **Verificar IP de red**: 
   - Windows: `ipconfig | findstr "IPv4"`
   - Linux/Mac: `ifconfig` o `ip addr`
2. **Actualizar .env**: Cambiar `VUE_APP_API_URL` a tu IP de red (ejemplo: `http://192.168.1.100:5000/api`)
3. **Reiniciar frontend**: `npm run serve`
4. **Verificar CORS**: Asegurar que el backend permita tu IP
5. **Verificar firewall**: Permitir conexiones en puerto 8080

### Error de Autenticación
1. Verificar que los tokens estén almacenados
2. Confirmar que no hayan expirado
3. Revisar la configuración de JWT
4. Comprobar los interceptores de Axios

### Error de Build
1. Verificar que todas las dependencias estén instaladas
2. Confirmar la versión de Node.js
3. Revisar la configuración de Vue CLI
4. Comprobar los errores de linting

### Error de CORS
1. Verificar la configuración del backend
2. Confirmar que el frontend esté en el puerto correcto
3. Revisar los headers de las peticiones
4. Comprobar la configuración de proxy

## 📝 Tecnologías Utilizadas

- **Vue.js 3** - Framework frontend
- **Vue Router 4** - Navegación
- **Pinia** - Estado global
- **Bootstrap 5** - CSS framework
- **Bootstrap Icons** - Iconografía
- **Axios** - Cliente HTTP
- **Vue CLI** - Herramientas de desarrollo

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Jeraldyn** - [GitHub](https://github.com/Jeyac)

## 📚 Repositorio

**URL del Repositorio**: https://github.com/Jeyac/Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-.git

---

⭐ Si este proyecto te ha sido útil, ¡dale una estrella!
