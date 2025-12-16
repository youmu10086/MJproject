<template>
    <div class="not-found">
        <h1>404</h1>
        <p>抱歉，您访问的页面不存在。</p>
        <el-button type="primary" @click="goHome">返回首页</el-button>
    </div>
</template>

<script setup>
defineOptions({ name: 'NotFoundPage' });
import { useRouter } from 'vue-router';

const router = useRouter();
const goHome = () => {
    router.push('/'); // 跳转到首页
};
</script>

<style scoped>
.not-found {
    text-align: center;
    margin-top: 100px;
}

.not-found h1 {
    font-size: 100px;
    color: #f56c6c;
}

.not-found p {
    font-size: 18px;
    color: #606266;
}

.el-button {
    margin-top: 20px;
}
</style>