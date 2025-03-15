<template>
    <el-dialog v-model="userStore.loginDialogVisible" :title="isLogin ? '用户登录' : '用户注册'" width="500" class="auth-dialog"
        @closed="handleDialogClose">
        <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px" label-position="top"
            status-icon>
            <el-form-item label="账户名称" prop="username">
                <el-input v-model="formData.username" placeholder="请输入用户名" prefix-icon="User" clearable />
            </el-form-item>

            <el-form-item label="登录密码" prop="password">
                <el-input v-model="formData.password" type="password" placeholder="请输入密码" prefix-icon="Lock"
                    show-password clearable />
            </el-form-item>

            <el-form-item class="action-buttons">
                <el-button type="primary" @click="handleSubmit" :loading="isSubmitting">
                    {{ isLogin ? '立即登录' : '注册账户' }}
                </el-button>
                <el-button link @click="toggleAuthMode">
                    {{ isLogin ? '没有账户？立即注册' : '已有账户？立即登录' }}
                </el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/store/userStore';
import { ElMessage } from 'element-plus';
import apiClient from '@/services/apiClient';

const userStore = useUserStore();
const formRef = ref(null);
const isLogin = ref(true);
const isSubmitting = ref(false);
const formData = ref({
    username: '',
    password: ''
});

// 表单验证规则
const formRules = {
    username: [
        { required: true, message: '账户名称不能为空', trigger: 'blur' },
        {
            min: 3,
            max: 20,
            message: '用户名长度需为3-20个字符',
            trigger: ['blur']
        }
    ],
    password: [
        { required: true, message: '密码不能为空', trigger: 'blur' },
        {
            min: 6,
            max: 20,
            message: '密码长度需为6-20位',
            trigger: ['blur']
        }
    ]
};

// 处理弹窗关闭事件
const handleDialogClose = () => {
    formRef.value?.resetFields();
    isLogin.value = true;
};

// 切换认证模式
const toggleAuthMode = () => {
    isLogin.value = !isLogin.value;
    formRef.value?.clearValidate();
};

// 提交表单
const handleSubmit = async () => {
    try {
        await formRef.value.validate();
        isSubmitting.value = true;

        const response = await apiClient.post(isLogin.value ? 'login/' : 'enroll/', formData.value);

        userStore.$patch(state => {
            state.isLoggedIn = true;
            state.userInfo = {
                ...state.userInfo,
                name: response.data.username
            };
        });

        localStorage.setItem('accessToken', response.data.access);
        ElMessage.success(isLogin.value ? '登录成功' : '注册成功');
        userStore.loginDialogVisible = false;
    } catch (error) {
        const message = error.response?.data?.detail || '请求异常，请稍后重试';
        console.log(error)
        ElMessage.error(message);
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<style scoped>
.auth-dialog {
    --el-dialog-border-radius: 8px;
}

:deep(.el-dialog__header) {
    border-bottom: 1px solid var(--el-border-color-light);
    margin-bottom: 1.5rem;
}

.action-buttons {
    margin-top: 2rem;
}

.el-button {
    width: 100%;
    margin-left: 0;
}

.el-button+.el-button {
    margin-top: 1rem;
}
</style>