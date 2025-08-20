/**
 * Configuración de Vue CLI
 * ========================
 * 
 * Este archivo configura Vue CLI para el desarrollo y construcción de la aplicación:
 * - Configuración del servidor de desarrollo
 * - Configuración de webpack para optimización
 * - Configuración de variables de entorno
 * - Configuración de plugins y loaders
 * 
 * Características:
 * - Puerto de desarrollo configurado en 8080
 * - Optimizaciones de webpack para mejor rendimiento
 * - Configuración de variables de entorno de Vue
 * - Configuración del título de la aplicación
 */

const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  // Transpilar dependencias que no están en ES6
  transpileDependencies: true,
  
  // Deshabilitar ESLint temporalmente para evitar errores de configuración
  lintOnSave: false,
  
  // Configuración del servidor de desarrollo
  devServer: {
    host: '0.0.0.0', // Permitir acceso desde cualquier dispositivo en la red
    port: 8080, // Puerto donde se ejecutará el servidor de desarrollo
    open: false, // No abrir automáticamente el navegador
    hot: true,   // Habilitar hot reload
    historyApiFallback: true, // Para que Vue Router funcione correctamente
    allowedHosts: 'all' // Permitir todos los hosts
  },
  
  // Configuración de webpack
  chainWebpack: config => {
    // Configurar el título de la aplicación en el HTML
    config.plugin('html').tap(args => {
      args[0].title = 'Catálogo de Productos'
      return args
    })
  },
  
  // Configuración adicional de webpack
  configureWebpack: {
    plugins: [
      // Definir variables de entorno de Vue para eliminar warnings
      new webpack.DefinePlugin({
        // Habilitar Options API (necesario para algunos componentes)
        __VUE_OPTIONS_API__: JSON.stringify(true),
        
        // Deshabilitar devtools en producción
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
        
        // Deshabilitar detalles de hidratación en producción
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false)
      })
    ],
    
    // Optimizaciones de rendimiento
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          common: {
            name: 'chunk-common',
            minChunks: 2,
            priority: 5,
            chunks: 'initial',
            reuseExistingChunk: true
          }
        }
      }
    }
  },
  
  // Configuración de CSS
  css: {
    // Extraer CSS a archivos separados en producción
    extract: process.env.NODE_ENV === 'production',
    
    // Configuración de source maps
    sourceMap: process.env.NODE_ENV !== 'production'
  },
  
  // Configuración de producción
  productionSourceMap: false, // No generar source maps en producción
  
  // Configuración de assets
  assetsDir: 'static', // Directorio para assets estáticos
  
  // Configuración de public path
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/'
})
