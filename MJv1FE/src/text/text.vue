<!-- src/components/Login.vue -->
<template>
  <div>
    <h2>Login</h2>
    <!-- 登录表单 -->
    <form @submit.prevent="handleLogin">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Cookies from 'js-cookie';

const username = ref('');
const password = ref('');
const errorMessage = ref('');

// 模拟的登录函数，实际应用中应替换为对后端 API 的调用
const handleLogin = async () => {
  // 这里我们简单模拟一个令牌生成
  const generatedToken = 'your-generated-token-here'; // 在实际应用中，这个令牌应该来自后端

  // 设置 cookie，假设我们设置一个名为 'authToken' 的 cookie，并设置过期时间为 7 天
  Cookies.set('authToken', generatedToken, { expires: 7 });

  // 清除错误信息（如果有）
  errorMessage.value = '';

  // 在这里可以执行登录成功后的逻辑，比如重定向到另一个页面
  console.log('Login successful! Token set in cookie.');
};
</script>

<style scoped>
/* 添加一些基本的样式 */
form {
  display: flex;
  flex-direction: column;
}
input {
  margin-bottom: 1em;
  padding: 0.5em;
  font-size: 1em;
}
button {
  padding: 0.75em 1.5em;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #369a6f;
}
p {
  color: red;
}
</style>