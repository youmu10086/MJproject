<template>
  <div>
      <el-breadcrumb :separator-icon="ArrowRight" class="no-select">
          <el-breadcrumb-item to="/Home">首页</el-breadcrumb-item>
          <el-breadcrumb-item>员工管理</el-breadcrumb-item>
      </el-breadcrumb>

      <el-card class="main-card" title="添加员工" :body-style="{ padding: '20px' }">
          <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
              <el-form-item label="姓名" prop="name">
                  <el-input v-model="formData.name" placeholder="请输入员工姓名" />
              </el-form-item>

              <el-form-item label="密码" prop="password">
                  <el-input type="password" v-model="formData.password" placeholder="请输入员工密码" />
              </el-form-item>

              <el-form-item label="电子邮件" prop="email">
                  <el-input v-model="formData.email" placeholder="请输入员工邮箱" />
              </el-form-item>

              <el-form-item label="电话" prop="phone">
                  <el-input v-model="formData.phone" placeholder="请输入员工电话" />
              </el-form-item>

              <el-form-item label="职位" prop="role">
                  <el-radio-group v-model="formData.role">
                      <el-radio-button label="manager" value="manager">经理</el-radio-button>
                      <el-radio-button label="admin" value="admin">管理员</el-radio-button>
                  </el-radio-group>
              </el-form-item>

              <el-form-item class="action-buttons">
                  <el-button type="primary" @click="handleSubmit" :loading="isSubmitting">添加员工</el-button>
                  <el-button @click="resetForm">重置</el-button>
              </el-form-item>
          </el-form>
      </el-card>
  </div>
</template>

<script setup>

import { ref } from 'vue';
import { ArrowRight } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import apiClient from '@/services/apiClient';  // 确保您的 API 客户端路径正确  

const formRef = ref(null);
const isSubmitting = ref(false);

const formData = ref({
  name: '',
  email: '',
  phone: '',
  password: '',
  role: 'manager'  // 默认角色为 manager  
});

const formRules = {
  name: [
      { required: true, message: '姓名不能为空', trigger: 'blur' }
  ],
  password: [
      { required: true, message: '密码不能为空', trigger: 'blur' },
      { min: 6, max: 20, message: '密码长度需为6-20位', trigger: ['blur'] }
  ],
  email: [
      // { required: true, message: '电子邮件不能为空', trigger: 'blur' },  
      { type: 'email', message: '请输入有效的电子邮件', trigger: ['blur', 'change'] }
  ],
  phone: [
      // { required: true, message: '电话不能为空', trigger: 'blur' }  
  ],
  role: [
      { required: true, message: '职位不能为空', trigger: 'change' }
  ]
};

const handleSubmit = async () => {
  try {
      await formRef.value.validate();
      isSubmitting.value = true;

      // 发送请求到后端 API  
      const response = await apiClient.post('add_employee/', {
          name: formData.value.name,
          password: formData.value.password,
          email: formData.value.email,
          phone: formData.value.phone,
          role: formData.value.role,
      });
      resetForm();
      ElMessage.success('添加员工成功');
  }
  catch (error) { }
  finally { isSubmitting.value = false; }
};

const resetForm = () => {
  formData.value = {
      name: '',
      email: '',
      phone: '',
      password: '',
      role: 'manager'
  };
};  
</script>

<style scoped>
.main-card {
  margin: 20px;
}

.action-buttons {
  margin-top: 20px;
}
</style>