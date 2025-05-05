<template>
  <el-row>
    <el-col :span="23">
      <el-link href="/Home" style="font-weight: bold; font-size: 20px;">
        美家公寓
      </el-link>
    </el-col>
    <el-col :span="1">
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
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '@/store/userStore';
import { ElMessage } from 'element-plus';
import apiClient from '@/services/apiClient';
import { Setting } from '@element-plus/icons-vue';

const userStore = useUserStore();

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
  } catch (error) {}
};
</script>

<style scoped>
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
  transition: transform 0.3s ease; /* 添加平滑的旋转效果 */
}

.setting-button:hover {
  transform: rotate(90deg); /* 鼠标悬停时旋转 360 度 */
}
</style>