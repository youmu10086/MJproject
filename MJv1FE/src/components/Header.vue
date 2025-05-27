<template>
  <el-row class="header-container">
    <el-link @click="router.push('/home')" class="logo-text">
      美家公寓
    </el-link>
    <drop-down v-if="isMobile"></drop-down>
    <el-popover v-if="userStore.isLoggedIn" placement="bottom-end" trigger="hover" width="155">
      <template #reference>
        <el-avatar :title="userStore.userInfo.username" class="user-avatar">
          {{ nameInitial }}
        </el-avatar>
      </template>
      <div class="button-group">
        <el-button aria-label="退出登录" type="danger" plain @click="handleLogout">退出登录</el-button>
        <el-button aria-label="设置" type="primary" plain :icon="Setting" circle class="setting-button" />
      </div>
    </el-popover>
    <el-avatar v-else @click="userStore.loginDialogVisible = true" class="user-avatar">
      登录
    </el-avatar>
  </el-row>
</template>

<script setup lang="ts">
defineOptions({ name: 'HeaderComponent' });
import { computed } from 'vue';
import { useUserStore } from '@/store/userStore';
import { ElMessage } from 'element-plus';
import apiClient from '@/services/apiClient';
import { Setting } from '@element-plus/icons-vue';
import { useDeviceStore } from '@/store/deviceStore';
import DropDown from './DropDown.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const userStore = useUserStore();
const deviceStore = useDeviceStore();
const isMobile = computed(() => deviceStore.isMobile);

const nameInitial = computed(() =>
  userStore.userInfo.username?.charAt(0)?.toUpperCase() || ''
);

const handleLogout = async () => {
  try {
    await apiClient.post('logout/');
    userStore.resetUser();
    localStorage.removeItem('accessToken');
    ElMessage.success('已安全退出');
    setTimeout(() => {
      window.location.href = '/home';
    }, 1000);
  } catch { /*empty*/ }
};
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logo-text {
  font-weight: bold;
  font-size: 20px;
}

.user-avatar {
  cursor: pointer;
  transition: transform 0.2s;
}

.user-avatar:hover {
  transform: scale(1.1);
}

.button-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.setting-button {
  transition: transform 0.3s ease;
}

.setting-button:hover {
  transform: rotate(90deg);
}
</style>