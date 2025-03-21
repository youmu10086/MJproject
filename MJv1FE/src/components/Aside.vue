<template>
    <el-row>
        <el-col :span="24">
            <el-menu active-text-color="#337ecc" background-color="#ffffff" @select="handleSelect" text-color="#606266"
                router :default-active="$route.path.replace('/', '')">
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
                        <Box />
                    </el-icon>
                    <span>住房用品管理</span>
                </el-menu-item>
                <el-menu-item index="roomReservation" v-if="userStore.isCustomer||userStore.isGuest">
                    <el-icon><House /></el-icon>
                    <span>预订房间</span>
                </el-menu-item>
                <el-menu-item index="reservationManage" v-if="userStore.isCustomer||userStore.isGuest">
                    <el-icon><More /></el-icon>
                    <span>预订管理</span>
                </el-menu-item>
                <el-menu-item index="onlineService" v-if="userStore.isCustomer||userStore.isGuest">
                    <el-icon><Service /></el-icon>
                    <span>在线客服</span>
                </el-menu-item>
                <el-menu-item index="reviewsFeedback" v-if="userStore.isCustomer||userStore.isGuest">
                    <el-icon><Comment /></el-icon>
                    <span>评价反馈</span>
                </el-menu-item>
                <el-menu-item index="staffManage" v-if="userStore.isAdmin">
                    <el-icon><Comment /></el-icon>
                    <span>staff管理</span>
                </el-menu-item>
            </el-menu>
        </el-col>
    </el-row>
</template>

<script setup>
import { UserFilled, Avatar, HomeFilled, Box, } from '@element-plus/icons-vue';
import { useUserStore } from '@/store/userStore';
import { useRouter } from 'vue-router';
import { ref } from 'vue'

const userStore = useUserStore();

const activeMenu = ref('manage')

const router = useRouter();
// 开始时请求表的数据
const handleSelect = (index) => {
    activeMenu.value = index;
    router.push(`/${index}`); // 路由切换
};

</script>

<style scoped></style>