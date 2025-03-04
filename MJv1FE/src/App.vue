<template>
    <el-container>
        <el-header style="height: 60px;">
            <el-row>
                <el-col :span="18">
                    美佳公寓
                </el-col>
                <el-col :span="1" style="display: flex; align-items: center; justify-content: center;">
                    <el-avatar src="src\components\icons\03b0d39583f48206768a7534e55bcpng.png" />
                </el-col>
            </el-row>
        </el-header>
        <el-container style="height: 100vh; overflow: hidden;">
            <el-aside width="150px">
                <el-row class="tac">
                    <el-col :span="24">
                        <el-menu active-text-color="#337ecc" background-color="#ffffff"
                            class="el-menu-vertical-demo no-select" @select="handleSelect" text-color="#606266">
                            <el-menu-item index="customer">
                                <!-- 图标 -->
                                <el-icon>
                                    <UserFilled />
                                </el-icon>
                                <router-link to="/customer"
                                    style="text-decoration: none; color: inherit">入住人员管理</router-link>
                            </el-menu-item>
                            <el-menu-item index="employee">
                                <el-icon>
                                    <Avatar />
                                </el-icon>
                                <router-link to="/employee"
                                    style="text-decoration: none; color: inherit">公寓职工管理</router-link>
                            </el-menu-item>
                            <el-menu-item index="room">
                                <el-icon>
                                    <HomeFilled />
                                </el-icon>
                                <router-link to="/room"
                                    style="text-decoration: none; color: inherit">公寓房间管理</router-link>
                            </el-menu-item>
                            <el-menu-item index="supplies">
                                <el-icon>
                                    <Box />
                                </el-icon>
                                <router-link to="/supplies"
                                    style="text-decoration: none; color: inherit">住房用品管理</router-link>
                            </el-menu-item>
                        </el-menu>
                    </el-col>
                </el-row>
            </el-aside>
            <el-container>
                <el-main :style="{ height: mainHeight }">
                    <router-view></router-view>
                </el-main>
                <el-footer style="height: 30px;"><el-text class="mx-1" type="info">美佳公寓管理系统 ©
                        2024.版权所有cyf.</el-text></el-footer>
            </el-container>
        </el-container>
    </el-container>
    <el-backtop :right="100" :bottom="100" />
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router';
import { UserFilled, Avatar, HomeFilled, Box, ArrowRight, } from '@element-plus/icons-vue';
const header = ref(null); // 引用头部元素  
const footer = ref(null); // 引用底部元素  
const mainHeight = ref(''); // 用于存储 el-main 的动态高度  

// 更新 el-main 高度的函数  
const updateMainHeight = () => {
    const headerHeight = header.value ? header.value.clientHeight : 0; // 获取头部高度  
    const footerHeight = footer.value ? footer.value.clientHeight : 0; // 获取底部高度  
    // 计算 el-main 的高度，使其在视口高度中减去头部和底部的高度  
    mainHeight.value = `calc(100vh - ${headerHeight + footerHeight}px)`;
};

// 组件挂载时调用，设置初始高度并添加窗口大小变化的事件监听  
onMounted(() => {
    updateMainHeight(); // 初始计算高度  
    window.addEventListener('resize', updateMainHeight); // 窗口大小变化时更新高度  
});

// 组件卸载前调用，移除事件监听器  
onBeforeUnmount(() => {
    window.removeEventListener('resize', updateMainHeight);
});

const activeMenu = ref('customer')

const router = useRouter();
// 开始时请求表的数据
const handleSelect = (index) => {
    activeMenu.value = index;
    router.push(`/${index}`);  // 路由切换  
};

</script>

<style>
html,
#app,
body,
.el-container {
    margin: 0px;
    padding: 0px;
    height: 100%;
}

.el-header {
    background-color: #d9ecff;
    color: #333;
    font-weight: bold;
    line-height: 60px;
}

.el-footer {
    background-color: #ecf5ff;
    color: #333;
    text-align: center;
    font-size: 15px;
    line-height: 30px;
}

.el-aside {
    background-color: #d9ecff;
    color: #333;
    text-align: center;
    /* line-height: 150px; */
}

.el-main {
    background-color: #ecf5ff;
    color: #333;
}

body.el-container {
    margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
    line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
    line-height: 320px;
}

.no-select {
    -webkit-user-select: none;
    /* Safari */
    -moz-user-select: none;
    /* Firefox */
    -ms-user-select: none;
    /* Internet Explorer/Edge */
    user-select: none;
    /* Non-prefixed version, currently supported by Chrome, Opera */
}

.demo-pagination-block+.demo-pagination-block {
    margin-top: 10px;
}

.demo-pagination-block .demonstration {
    margin-bottom: 16px;
}

html,
body {
    overflow: hidden;
    /* 禁止全局滚动 */
    height: 100%;
    margin: 0;
}

.el-main {
    overflow-y: auto;
    /* 仅让 el-main 滚动 */
}

/* 标记不允许用户选择文本 */
.no-select {
    -webkit-user-select: none;
    /* Safari */
    -moz-user-select: none;
    /* Firefox */
    -ms-user-select: none;
    /* Internet Explorer/Edge */
    user-select: none;
    /* Non-prefixed version, currently supported by Chrome, Opera */
}
</style>
