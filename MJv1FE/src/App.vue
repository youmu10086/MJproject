<template>
  <el-container style="height: 100vh; display: flex; flex-direction: column;">
    <el-header style="height: 60px;">
      <Header></Header>
    </el-header>
    <el-container style="flex: 1; display: flex; position: relative;">
      <Aside v-if="deviceStore.isComputer" class="sidebar"></Aside>
      <el-main
        :style="{ marginLeft: deviceStore.isComputer ? '70px' : '0px', flex: 1, position: 'relative', zIndex: 1, transition: 'margin-left 0.3s ease' }">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <el-scrollbar>

              <component :is="Component" />
            </el-scrollbar>
          </transition>
        </router-view>
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

import { useDeviceStore } from "@/store/deviceStore";

const deviceStore = useDeviceStore();

</script>

<style lang="scss" scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.sidebar {
  position: absolute;
  top: 0;
  bottom: 0;
  z-index: 2;
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
}

.el-main {
  background-color: var(--footer-bg-color);
  color: var(--text-color);
  // overflow-y: auto;
  height: calc(100vh - 60px);
  padding: 20px;
}

.no-select {
  -webkit-user-select: none;
  user-select: none;
}
</style>