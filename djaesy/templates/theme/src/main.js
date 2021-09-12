import { createApp } from 'vue'
import App from './App.vue'
import GAuth from 'vue3-google-oauth2'
import './index.css'
import router from "./router"
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/lib/theme-chalk/index.css'
import Maska from 'maska'

const gAuthOptions = { clientId: '578655982087-b0878kv0a4hlqcubg590nkm2u1n8f2u9.apps.googleusercontent.com'}

const app = createApp(App)
app.directive('maska', Maska.maska);
app.use(router).use(store).use(GAuth, gAuthOptions).use(ElementPlus).mount('#app')

//import "./index.css"
//console.log('Joia ou não...');

