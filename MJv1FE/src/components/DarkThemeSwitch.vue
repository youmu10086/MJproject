<template>
    <el-switch v-model="isLight" style="margin-left: 24px" inline-prompt :active-icon="Sunny" :inactive-icon="Moon"
        class="custom-switch" />
</template>

<script setup lang="ts">
defineOptions({ name: 'DarkThemeSwitch' });
import { Moon, Sunny } from '@element-plus/icons-vue';
import { useDark } from '@vueuse/core';
import { computed } from 'vue';

const isDark = useDark(); // 检测当前是否为深色模式
const isLight = computed({
    get: () => !isDark.value,
    set: (value) => (isDark.value = !value),
});
</script>

<style scoped></style>