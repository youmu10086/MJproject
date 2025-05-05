<!-- src/components/WebSocketTest.vue -->
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const socket = ref(null)
const connectionStatus = ref('Disconnected')
const receivedMessages = ref([])
const inputMessage = ref('')
const log = ref('')

const connectWebSocket = () => {
    // 开发环境用localhost，生产环境换成你的域名
    const wsUrl = import.meta.env.DEV
        ? 'ws://localhost:8000/ws/test/'
        : 'wss://yourdomain.com/ws/test/'

    socket.value = new WebSocket(wsUrl)

    socket.value.onopen = () => {
        connectionStatus.value = 'Connected'
        addLog('WebSocket connection established')
    }

    socket.value.onmessage = (event) => {
        const data = JSON.parse(event.data)
        receivedMessages.value.push(data.message)
        addLog(`Received: ${data.message}`)
    }

    socket.value.onerror = (error) => {
        addLog(`WebSocket error: ${error}`)
    }

    socket.value.onclose = () => {
        connectionStatus.value = 'Disconnected'
        addLog('WebSocket connection closed')
    }
}

const sendMessage = () => {
    if (inputMessage.value.trim() && socket.value?.readyState === WebSocket.OPEN) {
        socket.value.send(JSON.stringify({
            message: inputMessage.value
        }))
        addLog(`Sent: ${inputMessage.value}`)
        inputMessage.value = ''
    }
}

const disconnectWebSocket = () => {
    if (socket.value) {
        socket.value.close()
    }
}

const addLog = (message) => {
    log.value += `[${new Date().toLocaleTimeString()}] ${message}\n`
}

onMounted(() => {
    connectWebSocket()
})

onUnmounted(() => {
    disconnectWebSocket()
})
</script>

<template>
    <div class="websocket-test">
        <h2>WebSocket Connection Test</h2>

        <div class="status">
            Connection Status: <span :class="connectionStatus.toLowerCase()">{{ connectionStatus }}</span>
        </div>

        <div class="controls">
            <button @click="connectWebSocket" :disabled="socket?.readyState === WebSocket.OPEN">
                Connect
            </button>
            <button @click="disconnectWebSocket" :disabled="!socket || socket.readyState === WebSocket.CLOSED">
                Disconnect
            </button>
        </div>

        <div class="message-box">
            <input v-model="inputMessage" @keyup.enter="sendMessage" placeholder="Type a message..."
                :disabled="!socket || socket.readyState !== WebSocket.OPEN">
            <button @click="sendMessage"
                :disabled="!socket || socket.readyState !== WebSocket.OPEN || !inputMessage.trim()">
                Send
            </button>
        </div>

        <div class="messages">
            <h3>Received Messages:</h3>
            <ul>
                <li v-for="(msg, index) in receivedMessages" :key="index">
                    {{ msg }}
                </li>
            </ul>
        </div>

        <div class="event-log">
            <h3>Event Log:</h3>
            <pre>{{ log }}</pre>
        </div>
    </div>
</template>

<style scoped>
.websocket-test {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
}

.status {
    margin: 10px 0;
    padding: 10px;
    background: #f5f5f5;
    border-radius: 4px;
}

.status span {
    font-weight: bold;
}

.status span.connected {
    color: green;
}

.status span.disconnected {
    color: red;
}

.controls {
    margin: 15px 0;
}

.controls button {
    margin-right: 10px;
    padding: 5px 10px;
}

.message-box {
    margin: 15px 0;
    display: flex;
    gap: 10px;
}

.message-box input {
    flex-grow: 1;
    padding: 8px;
}

.messages {
    margin: 15px 0;
    border: 1px solid #ddd;
    padding: 10px;
    min-height: 100px;
    max-height: 200px;
    overflow-y: auto;
}

.event-log {
    margin-top: 20px;
    border: 1px solid #ddd;
    padding: 10px;
    background: #f9f9f9;
    max-height: 200px;
    overflow-y: auto;
}

pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 0;
}
</style>