import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import zhCn from "element-plus/es/locale/lang/zh-cn"; // 引入中文语言包
import router from "./router/index"; // 导入路由
import "element-plus/theme-chalk/dark/css-vars.css";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import "@/styles/main.scss";

import VChart from 'vue-echarts'; // 导入 vue-echarts
import * as echarts from 'echarts/core'; // 导入 ECharts 核心模块
import { CanvasRenderer } from 'echarts/renderers'; // 导入 Canvas 渲染器
import { RadarChart } from 'echarts/charts'; // 导入雷达图
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'; // 导入组件
echarts.use([CanvasRenderer, RadarChart, TitleComponent, TooltipComponent, LegendComponent]);

// 创建 Vue 应用实例
const app = createApp(App);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

// 引入图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}
// 使用 Element Plus 插件
app.use(ElementPlus, { locale: zhCn });
app.component('v-chart', VChart);
app.use(router);
app.use(pinia);
// 挂载应用实例
app.mount("#app");
