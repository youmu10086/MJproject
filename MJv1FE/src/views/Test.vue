<template>
    <button @click="sb">getenroll</button>
</template>

<script setup lang="ts">
import axios from 'axios';
import { useUserStore } from '@/store/userStore';

const apiClient = axios.create({
    baseURL: '/api',
});

const userStore = useUserStore();

const getenroll = () => {
    const user = { username: '666666', email: '666666', password: '666666' };

    apiClient.post("enroll/", user)
        .then((res) => {
            // 存储 Access Token
            console.log(res);
            localStorage.setItem('accessToken', res.data.access);
        })
        .catch((err) => {
            console.log(err);
        });
};

const sb = () => {
    console.log(userStore.isLoggedIn);

    console.log(userStore.role)
}
</script>

<style scoped></style>