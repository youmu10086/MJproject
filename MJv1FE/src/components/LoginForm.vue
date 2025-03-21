<template>
    <el-dialog v-model="userStore.loginDialogVisible" :title="formStatusTitle" width="500" class="auth-dialog"
        @closed="handleDialogClose">
        <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px" label-position="top"
            status-icon>
            <el-form-item label="账户名称" prop="username">
                <el-input v-model="formData.username" placeholder="请输入用户名" prefix-icon="User" clearable />
            </el-form-item>

            <el-form-item v-if="formStatus === 'enroll'" label="账户邮箱" prop="email">
                <el-input v-model="formData.email" placeholder="请输入邮箱" prefix-icon="Email" clearable />
            </el-form-item>

            <el-form-item label="登录密码" prop="password">
                <el-input v-model="formData.password" type="password" placeholder="请输入密码" prefix-icon="Lock"
                    show-password clearable />
            </el-form-item>

            <!-- 新增密码重置字段 -->
            <el-form-item v-if="formStatus === 'resetPassword'" label="确认密码" prop="confirmPassword">
                <el-input v-model="formData.confirmPassword" type="password" placeholder="请再次输入新密码" prefix-icon="Lock"
                    show-password clearable />
            </el-form-item>

            <!-- 主要操作按钮 -->
            <el-form-item class="action-buttons">
                <el-button type="primary" @click="handleSubmit" :loading="isSubmitting">
                    {{ submitButtonContent }}
                </el-button>
            </el-form-item>

            <el-form-item class="action-buttons">
                <div class="link-buttons">
                    <el-button link @click="toggleAuthMode">
                        {{ setButtonContent }}
                    </el-button>
                    <el-button v-show="formStatus === 'login'" link @click="setFormStatusIsReset">忘记密码？</el-button>
                </div>
            </el-form-item>
        </el-form>
    </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useUserStore } from '@/store/userStore';
import { ElMessage } from 'element-plus';
import apiClient from '@/services/apiClient';
import CryptoJS from 'crypto-js';

const userStore = useUserStore();
const formRef = ref(null);

const formStatus = ref('login'); // 'login', 'resetPassword', 'enroll'

const isSubmitting = ref(false);
const formData = ref({
    username: '666666',
    password: '666666',
    email: '',
});

// 表单验证规则  
const formRules = computed(() => ({
    username: [
        { required: true, message: '账户名称不能为空', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度需为3-20个字符', trigger: ['blur'] }
    ],
    email: [
        { type: 'email', message: '请输入有效的电子邮件', trigger: ['blur', 'change'] }
    ],
    password: [
        { required: true, message: '密码不能为空', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度需为6-20位', trigger: ['blur'] }
    ],
    confirmPassword: [
        {
            validator: (rule, value, callback) => {
                if (formStatus.value === 'resetPassword' && value !== formData.value.password) {
                    callback(new Error('两次输入的密码不一致'));
                } else {
                    callback();
                }
            },
            trigger: ['blur']
        }
    ]
}));

// 计算属性用于动态标题
const formStatusTitle = computed(() => {
    if (formStatus.value === 'login') return '用户登录';
    else if (formStatus.value === 'enroll') return '用户注册';
    else return '重置密码';
});

const submitButtonContent = computed(() => {
    if (formStatus.value === 'login') return '立刻登录';
    else if (formStatus.value === 'enroll') return '注册账户';
    else return '确认重置';
});

const setButtonContent = computed(() => {
    if (formStatus.value === 'login') return '没有账户？立即注册';
    else if (formStatus.value === 'enroll') return '已有账户？立即登录';
    else return '记起来了？返回登录';
});


const setFormStatusIsReset = () => {
    formStatus.value = 'resetPassword'
    formRef.value?.clearValidate();
}

// 处理弹窗关闭事件  
const handleDialogClose = () => {
    formRef.value?.resetFields();
    formStatus.value = 'login';
};

// 切换认证模式  
const toggleAuthMode = () => {
    console.log(formStatus.value)
    if (formStatus.value === 'login') formStatus.value = 'enroll';
    else if (formStatus.value === 'enroll') formStatus.value = 'login';
    else if (formStatus.value === 'resetPassword') formStatus.value = 'login';
    formRef.value?.clearValidate();
};

const resetPassword = () => {
    console.log("resetPassword")
}

// 提交表单  
const handleSubmit = async () => {

    if (formStatus.value === 'resetPassword') {
        try {
            await formRef.value.validate();
            isSubmitting.value = true;

            const encryptedPassword = CryptoJS.SHA256(formData.value.password).toString();

            const response = await apiClient.post('reset_password/', {
                username: formData.value.username,
                email: formData.value.email,
                password: encryptedPassword,
            });

            if (response.data.code === 1) {
                ElMessage.success('密码重置成功');
                userStore.loginDialogVisible = false;
            }
        } catch (error) {
            ElMessage.error(error.response?.data?.msg || '密码重置失败');
        } finally {
            isSubmitting.value = false;
        }
    }
    else {
        try {
            await formRef.value.validate();
            isSubmitting.value = true;

            const encryptedPassword = CryptoJS.SHA256(formData.value.password).toString();

            const response = await apiClient.post(formStatus.value === 'login' ? 'login/' : 'enroll/', {
                username: formData.value.username,
                password: encryptedPassword,
                email: formData.value.email,
            });

            userStore.$patch(state => {
                state.isLoggedIn = true;
                state.role = response.data.role;
                state.userInfo = {
                    ...state.userInfo,
                    name: response.data.username
                };
            });

            localStorage.setItem('accessToken', response.data.access);
            setTimeout(() => {
                window.location.href = '/home';
            }, 1000);
            ElMessage.success(formStatus.value === 'login' ? '登录成功' : '注册成功');
            userStore.loginDialogVisible = false;
        }
        catch (error) { }
        finally { isSubmitting.value = false; }
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
    margin-top: 1rem;
}

.link-buttons {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 0.5rem;
}

.el-button {
    width: 100%;
    margin-left: 0;
}

.el-button--link {
    padding: 0;
    margin: 0;
}
</style>