<template>
    <el-menu active-text-color="var(--menu-active-text-color)" background-color="var(--menu-background-color)"
        text-color="var(--menu-text-color)" router :default-active="$route.path.replace('/', '')" @select="handleSelect"
        :collapse="isCollapse" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
        <el-menu-item index="customer" v-if="userStore.isManager" class="menu-item">
            <el-icon class="menu-icon">
                <UserFilled />
            </el-icon>
            <span>入住人员管理</span>
        </el-menu-item>
        <el-menu-item index="employee" v-if="userStore.isManager" class="menu-item">
            <el-icon class="menu-icon">
                <Avatar />
            </el-icon>
            <span>公寓职工管理</span>
        </el-menu-item>
        <el-menu-item index="room" v-if="userStore.isManager" class="menu-item">
            <el-icon class="menu-icon">
                <HomeFilled />
            </el-icon>
            <span>公寓房间管理</span>
        </el-menu-item>
        <el-menu-item index="supplies" v-if="userStore.isManager">
            <el-icon class="menu-icon">
                <Briefcase />
            </el-icon>
            <span>住房用品管理</span>
        </el-menu-item>
        <el-menu-item index="room" v-if="userStore.isCustomer || userStore.isGuest" class="menu-item">
            <el-icon class="menu-icon">
                <House />
            </el-icon>
            <span>预订房间</span>
        </el-menu-item>
        <el-menu-item index="reservationManage" v-if="userStore.isCustomer" class="menu-item">
            <el-icon class="menu-icon">
                <More />
            </el-icon>
            <span>我的订单</span>
        </el-menu-item>
        <el-menu-item index="onlineService" v-if="userStore.isCustomer || userStore.isGuest" class="menu-item">
            <el-icon class="menu-icon">
                <Service />
            </el-icon>
            <span>在线客服</span>
        </el-menu-item>
        <el-menu-item index="userManage" v-if="userStore.isAdmin">
            <el-icon>
                <SwitchFilled />
            </el-icon>
            <span>用户管理</span>
        </el-menu-item>
    </el-menu>
</template>

<script setup lang="ts">
defineOptions({ name: 'AsideComponent' });

import { UserFilled, Avatar, HomeFilled, Briefcase, House, More, Service, SwitchFilled } from '@element-plus/icons-vue';
import { useUserStore } from '@/store/userStore';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const userStore = useUserStore();
const activeMenu = ref('');
const router = useRouter();

// 路由切换
const handleSelect = (index: string) => {
    activeMenu.value = index;
    router.push(`/${index}`);
};

// 控制菜单折叠状态
const isCollapse = ref(true);

// 防抖函数
let debounceTimer: number | null = null;
const debounce = (callback: () => void, delay: number) => {
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = window.setTimeout(callback, delay);
};

// 鼠标进入时展开菜单
const handleMouseEnter = () => {
    debounce(() => {
        isCollapse.value = false;
    }, 200); // 延迟 200ms
};

// 鼠标离开时折叠菜单
const handleMouseLeave = () => {
    debounce(() => {
        isCollapse.value = true;
    }, 300); // 延迟 300ms
};
</script>

<style scoped lang="scss">
.menu-item:hover {
    transform: translateX(-5px);
    /* 放大并向上移动 5px */
}

.menu-item {
  display: flex;
  align-items: center;
  transition: transform 0.3s ease; /* 添加平滑过渡效果 */
}

.menu-icon {
  transition: transform 0.3s ease; /* 添加平滑过渡效果 */
}
</style>