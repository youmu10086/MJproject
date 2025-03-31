<template>
    <el-row :class="{ dark: isDark, light: !isDark }">
        <el-col :span="24">
            <el-menu active-text-color="var(--menu-active-text-color)" background-color="var(--menu-background-color)"
                text-color="var(--menu-text-color)" router :default-active="$route.path.replace('/', '')"
                @select="handleSelect">
                <el-menu-item index="customer" v-if="userStore.isManager">
                    <el-icon>
                        <UserFilled />
                    </el-icon>
                    <span>入住人员管理</span>
                </el-menu-item>
                <el-menu-item index="employee" v-if="userStore.isManager">
                    <el-icon>
                        <Avatar />
                    </el-icon>
                    <span>公寓职工管理</span>
                </el-menu-item>
                <el-menu-item index="roomManage" v-if="userStore.isManager">
                    <el-icon>
                        <HomeFilled />
                    </el-icon>
                    <span>公寓房间管理</span>
                </el-menu-item>
                <el-menu-item index="supplies" v-if="userStore.isManager">
                    <el-icon>
                       <Briefcase />
                    </el-icon>
                    <span>住房用品管理</span>
                </el-menu-item>
                <el-menu-item index="roomReservation" v-if="userStore.isCustomer || userStore.isGuest">
                    <el-icon>
                        <House />
                    </el-icon>
                    <span>预订房间</span>
                </el-menu-item>
                <el-menu-item index="reservationManage" v-if="userStore.isCustomer || userStore.isGuest">
                    <el-icon>
                        <More />
                    </el-icon>
                    <span>预订管理</span>
                </el-menu-item>
                <el-menu-item index="onlineService" v-if="userStore.isCustomer || userStore.isGuest">
                    <el-icon>
                        <Service />
                    </el-icon>
                    <span>在线客服</span>
                </el-menu-item>
                <el-menu-item index="reviewsFeedback" v-if="userStore.isCustomer || userStore.isGuest">
                    <el-icon>
                        <Comment />
                    </el-icon>
                    <span>评价反馈</span>
                </el-menu-item>
                <el-menu-item index="userManage" v-if="userStore.isAdmin">
                    <el-icon>
                        <SwitchFilled />
                    </el-icon>
                    <span>用户管理</span>
                </el-menu-item>
            </el-menu>
        </el-col>
    </el-row>
</template>

<script setup>
import { UserFilled, Avatar, HomeFilled, Briefcase, House, More, Service, Comment, SwitchFilled } from '@element-plus/icons-vue';
import { useUserStore } from '@/store/userStore';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { useDark } from '@vueuse/core';

const userStore = useUserStore();
const activeMenu = ref('manage');
const router = useRouter();

// 主题切换逻辑
const isDark = useDark(); // 检测当前是否为深色模式

// 路由切换
const handleSelect = (index) => {
    activeMenu.value = index;
    router.push(`/${index}`);
};
</script>

<style scoped>
.el-menu-item {
    border-right: none !important;
}

.dark {
    --menu-active-text-color: #337ecc;
    --menu-background-color: #141414;
    --menu-text-color: #ffffff;
}

.light {
    --menu-active-text-color: #337ecc;
    --menu-background-color: #ffffff;
    --menu-text-color: #606266;
}

.el-menu {
    transition: background-color 0.3s ease, color 0.3s ease;
    margin-top: 20px;
}

.el-menu-item {
    font-size: 12px;
    color: var(--menu-text-color);
}

.el-menu-item:hover {
    color: var(--menu-active-text-color);
    background-color: var(--menu-background-color);
}
</style>