import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'; // 引入中文语言包   
import router from './router'; // 导入路由  
import 'element-plus/theme-chalk/dark/css-vars.css'


// 创建 Vue 应用实例
const app = createApp(App)  

// 引入图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
// 使用 Element Plus 插件  
app.use(ElementPlus, { locale: zhCn });
app.use(router);
// 挂载应用实例
app.mount('#app');