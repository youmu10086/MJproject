<template>
  <el-container style="height: 100vh; display: flex; flex-direction: column;">
    <el-header style="height: 60px;">
      <Header></Header>
    </el-header>
    <el-container style="flex: 1; display: flex; position: relative; overflow: hidden;">
      <!-- Aside 使用绝对定位 -->
      <Aside v-if="deviceStore.isComputer" class="sidebar"></Aside>
      <!-- el-main 动态调整 margin-left -->
      <el-main
        :style="{ marginLeft: deviceStore.isComputer ? '70px' : '0px', flex: 1, overflowY: 'auto', position: 'relative', zIndex: 1, transition: 'margin-left 0.3s ease' }">
        <el-scrollbar>
          <router-view></router-view>
        </el-scrollbar>
      </el-main>
    </el-container>
  </el-container>

  <LoginForm></LoginForm>
  <FloatButton></FloatButton>
  <MessageCard></MessageCard>
</template>
<script setup lang="ts">
import LoginForm from './components/LoginForm.vue';
import Header from './components/Header.vue';
import Aside from './components/Aside.vue';
import FloatButton from './components/DarkThemeFloatButton.vue';
import MessageCard from './components/MessageCard.vue';

import { useDeviceStore } from "@/store/device";

const deviceStore = useDeviceStore();

</script>

<style lang="scss" scoped>
.sidebar {
  position: absolute;
  top: 0;
  bottom: 0;
  z-index: 2;
}
</style>