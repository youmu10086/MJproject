<template>
    <div class="websocket-test">
      <h2>WebSocket Test</h2>
  
      <!-- 连接状态 -->
      <div class="status">
        Status: <span :class="connectionStatus.toLowerCase()">{{ connectionStatus }}</span>
      </div>
  
      <!-- 控制按钮 -->
      <div class="controls">
        <button @click="connectWebSocket" :disabled="isConnected">Connect</button>
        <button @click="disconnectWebSocket" :disabled="!isConnected">Disconnect</button>
      </div>
  
      <!-- 消息输入框 -->
      <div class="message-box">
        <input
          v-model="inputMessage"
          placeholder="Type a message..."
          :disabled="!isConnected"
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage" :disabled="!isConnected || !inputMessage.trim()">Send</button>
      </div>
  
      <!-- 接收的消息 -->
      <div class="messages">
        <h3>Messages:</h3>
        <ul>
          <li v-for="(msg, index) in receivedMessages" :key="index">{{ msg }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  
  const socket = ref(null); // WebSocket 实例
  const connectionStatus = ref('Disconnected'); // 连接状态
  const receivedMessages = ref([]); // 接收到的消息
  const inputMessage = ref(''); // 输入的消息
  
  // 是否已连接
  const isConnected = computed(() => connectionStatus.value === 'Connected');
  
  // 连接 WebSocket
  const connectWebSocket = () => {
    const wsUrl = import.meta.env.DEV
      ? 'ws://localhost:8001/ws/test/' // Django 开发环境 WebSocket 地址
      : 'wss://yourdomain.com/ws/test/'; // 生产环境 WebSocket 地址
  
    socket.value = new WebSocket(wsUrl);
  
    socket.value.onopen = () => {
      connectionStatus.value = 'Connected';
      console.log('WebSocket connected');
    };
  
    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data);
      receivedMessages.value.push(data.message);
      console.log('Message received:', data.message);
    };
  
    socket.value.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  
    socket.value.onclose = () => {
      connectionStatus.value = 'Disconnected';
      console.log('WebSocket disconnected');
    };
  };
  
  // 发送消息
  const sendMessage = () => {
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({ message: inputMessage.value }));
      console.log('Message sent:', inputMessage.value);
      inputMessage.value = '';
    }
  };
  
  // 断开 WebSocket
  const disconnectWebSocket = () => {
    if (socket.value) {
      socket.value.close();
    }
  };
  </script>
  
  <style scoped>
  .websocket-test {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .status {
    margin-bottom: 10px;
    font-weight: bold;
  }
  
  .status span.connected {
    color: green;
  }
  
  .status span.disconnected {
    color: red;
  }
  
  .controls {
    margin-bottom: 10px;
  }
  
  .controls button {
    margin-right: 10px;
  }
  
  .message-box {
    margin-bottom: 10px;
    display: flex;
    gap: 10px;
  }
  
  .message-box input {
    flex-grow: 1;
    padding: 5px;
  }
  
  .messages {
    border: 1px solid #ddd;
    padding: 10px;
    max-height: 150px;
    overflow-y: auto;
  }
  </style>