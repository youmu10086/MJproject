<template>
  <el-container>
    <el-header style="height: 60px;">
      <Header></Header>
    </el-header>
    <el-container style="height: 100vh; overflow: hidden;">
      <el-aside width="150px">
        <Aside></Aside>
      </el-aside>
      <el-container>
        <el-main :style="{ height: mainHeight }">
          <router-view></router-view>
          <LoginForm></LoginForm>
        </el-main>
        <el-footer style="height: 30px;"><el-text class="mx-1" type="info">美佳公寓管理系统 ©
            2024.版权所有cyf.</el-text></el-footer>
      </el-container>
    </el-container>
  </el-container>
  <el-backtop :right="100" :bottom="100" />
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import LoginForm from './components/LoginForm.vue';
import Header from './components/Header.vue';
import Aside from './components/Aside.vue';

const header = ref(null); // 引用头部元素
const footer = ref(null); // 引用底部元素
const mainHeight = ref(''); // 用于存储 el-main 的动态高度

// 更新 el-main 高度的函数
const updateMainHeight = () => {
  const headerHeight = header.value ? header.value.clientHeight : 0; // 获取头部高度
  const footerHeight = footer.value ? footer.value.clientHeight : 0; // 获取底部高度
  // 计算 el-main 的高度，使其在视口高度中减去头部和底部的高度
  mainHeight.value = `calc(100vh - ${headerHeight + footerHeight}px)`;
};

// 组件挂载时调用，设置初始高度并添加窗口大小变化的事件监听
onMounted(() => {
  updateMainHeight(); // 初始计算高度
  window.addEventListener('resize', updateMainHeight); // 窗口大小变化时更新高度
});

// 组件卸载前调用，移除事件监听器
onBeforeUnmount(() => {
  window.removeEventListener('resize', updateMainHeight);
});

</script>

<style>
/* 使用CSS变量定义颜色 */
:root {
  --header-bg-color: #d9ecff;
  --footer-bg-color: #ecf5ff;
  --text-color: #333;
}

html,
body,
#app {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

.el-container {
  height: 100%;
  margin-bottom: 0;
}

.el-header {
  background-color: var(--header-bg-color);
  color: var(--text-color);
  font-weight: bold;
  line-height: 60px;
}

.el-footer {
  background-color: var(--footer-bg-color);
  color: var(--text-color);
  text-align: center;
  font-size: 15px;
  line-height: 30px;
  position: absolute;
  /* 如果需要固定底部，可以添加这个并调整top属性 */
  bottom: 0;
  width: 100%;
}

.el-aside {
  background-color: var(--header-bg-color);
  color: var(--text-color);
  text-align: center;
  /* line-height: 可以根据实际需要调整或移除 */
}

.el-main {
  background-color: var(--footer-bg-color);
  color: var(--text-color);
  overflow-y: auto;
  height: calc(100vh - 60px - 30px);
}

.no-select {
  user-select: none;
}
</style>