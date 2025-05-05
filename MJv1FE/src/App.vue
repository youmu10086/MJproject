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
import LoginForm from './components/LoginForm.vue';
import Header from './components/Header.vue';
import Aside from './components/Aside.vue';
import FloatButton from './components/DarkThemeFloatButton.vue';
import MessageCard from './components/MessageCard.vue';
// import ProgressBar from './components/ProgressBar.vue';
</script>