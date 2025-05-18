const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  publicPath: '/static/',
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        logLevel: 'debug', // Добавь этот параметр для логирования
      },
    },
  },
});