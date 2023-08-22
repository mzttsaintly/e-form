import './assets/reset.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// vue3打印组件
import print from 'vue3-print-nb'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(print)

app.mount('#app')
