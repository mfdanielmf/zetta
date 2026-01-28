import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'

import App from './App.vue'
import router from './router'
import queryClient from './queries/queryClient'

const app = createApp(App)

app.use(createPinia())
app.use(VueQueryPlugin, { queryClient: queryClient })
app.use(router)

app.mount('#app')
