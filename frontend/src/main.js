// src/main.js
import { createApp }   from 'vue'
import { createPinia }  from 'pinia'
import App              from './App.vue'
import router           from './router'
import axios            from '@/services/api'    
import { useUiStore }   from '@/store/Ui.js'
import { registerPlugins } from '@/plugins'

const app = createApp(App)


const pinia = createPinia()
app.use(pinia)


app.use(router)
registerPlugins(app)


const uiStore = useUiStore()


axios.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      uiStore.authError = true
      console.log(uiStore.authError)
    }
    return Promise.reject(err)
  }
)

app.mount('#app')
