<template>
    <el-container>
      <el-header>
        <h2>登录页面</h2>
      </el-header>
      <el-main>
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="100px" class="demo-ruleForm">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="loginForm.password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">登录</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
  </template>
  
  <script setup>
  import { reactive, ref } from 'vue';
  import { ElMessage } from 'element-plus';
  
  // 定义表单数据
  const loginForm = reactive({
    username: '',
    password: ''
  });
  
  // 定义表单验证规则
  const rules = {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
    ]
  };
  
  // 使用 ref 获取表单引用
  const loginFormRef = ref(null);
  
  // 提交表单
  const submitForm = () => {
    loginFormRef.value.validate((valid) => {
      if (valid) {
        // 在这里添加你的登录逻辑，比如发送请求到后端
        console.log('提交表单:', loginForm);
        ElMessage.success('登录成功!');
      } else {
        console.log('表单验证失败!');
        return false;
      }
    });
  };
  
  // 重置表单
  const resetForm = () => {
    loginFormRef.value.resetFields();
  };
  </script>
  
  <style scoped>
  .demo-ruleForm {
    width: 300px;
    margin: 100px auto;
  }
  </style>