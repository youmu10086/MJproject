<template>
    <el-input v-model="inputMsg" @keyup.enter="send">
        <template #append>
            <el-button @click="send">发送</el-button>
        </template>
    </el-input>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const messages = ref([])
let socket = null

// 初始化连接
const initWebSocket = (roomId) => {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    socket = new WebSocket(`${protocol}://${location.host}/ws/chat/${roomId}/`)

    socket.onmessage = (e) => {
        messages.value.push(JSON.parse(e.data))
    }

    socket.onclose = () => {
        console.log('连接断开，尝试重连...')
        setTimeout(() => initWebSocket(roomId), 5000)  // 断线重连机制[6,8](@ref)
    }
}

onMounted(() => initWebSocket('general'))  // 默认进入公共聊天室
onBeforeUnmount(() => socket?.close())
const inputMsg = ref('')
const send = () => {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            user: '当前用户',
            content: inputMsg.value,
            timestamp: Date.now()
        }))
        inputMsg.value = ''
    }
}
</script>