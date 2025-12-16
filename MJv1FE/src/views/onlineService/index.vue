<template>
    <div>
        <el-breadcrumb :separator-icon="ArrowRight" class="no-select">
            <el-breadcrumb-item to="/Home">首页</el-breadcrumb-item>
            <el-breadcrumb-item>在线客服</el-breadcrumb-item>
        </el-breadcrumb>
        <div class="container">
            <div class="chat-window" >
                <div>本页面为客服演示界面，后端服务制作中</div>
                <div class="messages" >
                    <TransitionGroup name="message">
                        <div v-for="(message, index) in messages" :key="index"
                            :class="['message', message.sender === 'user' ? 'user' : 'service']">
                            <span>{{ message.text }}</span>
                        </div>
                    </TransitionGroup>
                </div>
                <div class="input-area">
                    <el-input v-model="inputMessage" placeholder="请输入消息..." @keyup.enter="sendMessage" />
                    <el-button type="primary" @click="sendMessage">发送</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { ArrowRight } from '@element-plus/icons-vue';

const messages = ref([
    { sender: 'service', text: '您好！有什么可以帮助您的吗？' },
    { sender: 'user', text: '我想了解一下房间预订的流程。' },
]);

const inputMessage = ref('');

const sendMessage = () => {
    if (inputMessage.value.trim()) {
        messages.value.push({ sender: 'user', text: inputMessage.value });
        inputMessage.value = '';

        setTimeout(() => {
            messages.value.push({
                sender: 'service',
                text: '好的，请稍等，我为您解答。',
            });
        }, 1000);
    }
};
</script>