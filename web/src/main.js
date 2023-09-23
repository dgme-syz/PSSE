import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import elmentIcon from "./plugins/icon"
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'

createApp(App).use(store).use(router).use(ElementPlus).use(elmentIcon).mount('#app')
