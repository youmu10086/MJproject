<template>
  <el-row>

    <el-link @click="router.push('/home')" style="font-weight: bold; font-size: 20px;">
      美家公寓
    </el-link>
    <div class="header-right">
      <drop-down v-if="isMobile"></drop-down>
      <div class="avatar-container">
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
      </div>
    </div>
  </el-row>
</template>

<script setup lang="ts">
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
  } catch (error) { }
};
</script>

<style scoped>
.header-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  position: absolute;
  right: 0px;
  /* 距离右边框 20px */
  top: 50%;
  /* 垂直居中 */
  transform: translateY(-50%);
  /* 修正垂直居中偏移 */
  gap: 20px;
  
  /* drop-down 和头像之间的间距 */
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
  /* 添加平滑的旋转效果 */
}

.setting-button:hover {
  transform: rotate(90deg);
  /* 鼠标悬停时旋转 90 度 */
}
</style>