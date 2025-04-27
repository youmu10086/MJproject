<template>
  <el-container style="height: 100vh; display: flex; flex-direction: column;">
    <el-header style="height: 60px;">
      <Header></Header>
    </el-header>
    <el-container style="flex: 1; display: flex; overflow: hidden;">
      <el-aside width="150px">
        <Aside></Aside>
      </el-aside>
      <el-main style="flex: 1; overflow-y: auto;">
        <el-scrollbar>
          <router-view></router-view>
          <LoginForm></LoginForm>
        </el-scrollbar>
      </el-main>
    </el-container>
  </el-container>

  <!-- 浮动按钮 -->
  <FloatButton></FloatButton>

  <!-- 消息卡片 -->
  <MessageCard></MessageCard>
</template>

<script setup lang="ts">
import '@/styles/main.scss'; // 引入样式主入口
import LoginForm from './components/LoginForm.vue';
import Header from './components/Header.vue';
import Aside from './components/Aside.vue';
import FloatButton from './components/DarkThemeFloatButton.vue';
import MessageCard from './components/MessageCard.vue';
import ProgressBar from './components/ProgressBar.vue';

</script>

<style >
/* 使用CSS变量定义颜色 */
:root {
  --header-bg-color: #FAFAFA;
  --footer-bg-color: #FFFFFF;
  --text-color: #333;
  --table-border-radius: 10px;
  --table-border-color: #dcdcdc;
}

.dark {
  --header-bg-color: #141414;
  --footer-bg-color: #141414;
  --text-color: #fff;
  --border-color: #333;
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
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.el-aside {
  background-color: var(--header-bg-color);
  color: var(--text-color);
  text-align: center;
  /* border-right: 1px solid #dcdcdc; */

}

.el-main {
  background-color: var(--footer-bg-color);
  color: var(--text-color);
  overflow-y: auto;
  height: calc(100vh - 55px);
  padding: 20px
}

.no-select {
  user-select: none;
}
</style>