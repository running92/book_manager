import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import {
  ArrowLeft,
  Collection,
  DataBoard,
  Folder,
  Lock,
  Notebook,
  Plus,
  Reading,
  Search,
  Setting,
  Tickets,
  Upload,
  User
} from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import i18n from './locales'
import './assets/styles.css'

const app = createApp(App)
const icons = { ArrowLeft, Collection, DataBoard, Folder, Lock, Notebook, Plus, Reading, Search, Setting, Tickets, Upload, User }
Object.entries(icons).forEach(([name, component]) => app.component(name, component))
app.use(createPinia())
app.use(router)
app.use(i18n)
app.use(ElementPlus)
app.mount('#app')
