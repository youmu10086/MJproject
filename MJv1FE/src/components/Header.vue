<template>  
  <el-row>  
    <el-col :span="23">  
      <el-link href="/Home" target="_blank" style="font-weight: bold; font-size: 20px;">  
        美家公寓  
      </el-link>  
    </el-col>  
    <el-col :span="1">  
      <el-popover   
        v-if="userStore.isLoggedIn"   
        placement="bottom-end"   
        trigger="hover"  
        @mouseleave="popoverVisible = false">  
        <template #reference>  
          <el-avatar   
            :title="userStore.userInfo.name"   
            class="user-avatar">  
            {{ nameInitial }}  
          </el-avatar>  
        </template>  
        <el-button type="danger" plain @click="handleLogout">  
          退出登录  
        </el-button>  
      </el-popover>  
      <el-avatar   
        v-else   
        @click="userStore.loginDialogVisible = true"   
        class="user-avatar">  
        登录  
      </el-avatar>  
    </el-col>  
  </el-row>  
</template>  

<script setup>  
import { computed } from 'vue'  
import { useUserStore } from '@/store/userStore'  
import { ElMessage } from 'element-plus'  
import apiClient from '@/services/apiClient'  

const userStore = useUserStore()  

const nameInitial = computed(() =>   
  userStore.userInfo.name?.charAt(0)?.toUpperCase() || ''  
)  

const handleLogout = async () => {  
  try {  
    await apiClient.post('logout/')  
    userStore.resetUser()  
    localStorage.removeItem('accessToken')  
    window.location.href = '/home';  
    ElMessage.success('已安全退出系统')  
  } catch (error) {  
    ElMessage.error('退出操作失败，请重试')  
  }  
}  
</script>  

<style scoped>  
.user-avatar {  
  cursor: pointer;  
  transition: transform 0.2s;  
}  

.user-avatar:hover {  
  transform: scale(1.1);  
}  
</style>  