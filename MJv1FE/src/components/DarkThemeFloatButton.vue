<template>
    <el-button :aria-label="isDark ? '切换到浅色模式' : '切换到深色模式'" class="float-button" type="primary" circle
        @click="toggleTheme()">
        <el-icon>
            <component :is="isDark ? Moon : Sunny" />
        </el-icon>
    </el-button>
</template>

<script setup lang="ts">
import { Moon, Sunny } from '@element-plus/icons-vue'; // 引入图标组件
import { useDark, useToggle } from '@vueuse/core';

const isDark = useDark(); // 检测当前是否为深色模式
const toggleTheme = useToggle(isDark); // 切换主题
</script>

<style scoped lang="scss">

.float-button:hover {
    transform: rotate(45deg);
}
</style>