<template>
    <div v-if="show" class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
</template>

<script setup>
import { ref } from "vue";

// 定义响应式变量
const show = ref(false);
const progress = ref(0);

// 定义方法
const start = () => {
    show.value = true;
    progress.value = 0;
};

const update = (value) => {
    progress.value = value;
};

const finish = () => {
    progress.value = 100;
    setTimeout(() => {
        show.value = false;
    }, 200);
};

const error = () => {
    progress.value = 100;
    show.value = false;
};
</script>

<style scoped>
.progress-bar-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: #f5f5f5;
    /* z-index: 9999; */
}

.progress-bar {
    height: 100%;
    background-color: #409eff;
    transition: width 0.3s ease;
}
</style>