import { createApp } from 'vue'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.css"
import "bootstrap/dist/js/bootstrap"
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')