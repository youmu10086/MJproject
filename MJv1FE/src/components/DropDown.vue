<template>
  <el-dropdown @command="handleCommand">
    <el-icon>
      <Menu />
    </el-icon>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="customer" v-if="userStore.isManager">
          入住人员管理
        </el-dropdown-item>
        <el-dropdown-item command="employee" v-if="userStore.isManager">
          公寓职工管理
        </el-dropdown-item>
        <el-dropdown-item command="room" v-if="userStore.isManager">
          公寓房间管理
        </el-dropdown-item>
        <el-dropdown-item command="supplies" v-if="userStore.isManager">
          住房用品管理
        </el-dropdown-item>
        <el-dropdown-item command="room" v-if="userStore.isCustomer || userStore.isGuest">
          预订房间
        </el-dropdown-item>
        <el-dropdown-item command="reservationManage" v-if="userStore.isCustomer">
          我的订单
        </el-dropdown-item>
        <el-dropdown-item command="onlineService" v-if="userStore.isCustomer || userStore.isGuest">
          在线客服
        </el-dropdown-item>
        <el-dropdown-item command="userManage" v-if="userStore.isAdmin">
          用户管理
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { useUserStore } from '@/store/userStore';
import { useRouter } from 'vue-router';
import { Menu, Setting, User } from '@element-plus/icons-vue'

const userStore = useUserStore();
const router = useRouter();

// 路由跳转逻辑
const handleCommand = (command: string) => {
  router.push(`/${command}`);
};
</script>

<style scoped>
.menu-icon {
  width: 24px;
  /* 设置图标宽度 */
  height: 24px;
  /* 设置图标高度 */
  cursor: pointer;
  /* 鼠标悬停时显示为手型 */
  border-radius: 50%;
  /* 如果需要圆形图标 */
  object-fit: cover;
  /* 确保图片按比例填充 */
}
</style>