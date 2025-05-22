<template>
    <div class="user-management">
        <!-- 面包屑导航 -->
        <el-breadcrumb :separator-icon="ArrowRight" class="no-select breadcrumb">
            <el-breadcrumb-item to="/Home">首页</el-breadcrumb-item>
            <el-breadcrumb-item>员工管理</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 添加员工表单 -->
        <el-card class="main-card" shadow="hover">
            <template #header>
                <div class="card-header">
                    <span class="header-title">添加新员工</span>
                    <div class="header-actions">
                        <el-button aria-label="提交" type="info" plain @click="resetForm">重置表单</el-button>
                    </div>
                </div>
            </template>

            <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
                <el-row :gutter="20">
                    <!-- 第一行 -->
                    <el-col :xs="24" :sm="12" :md="10">
                        <el-form-item label="员工姓名" prop="name">
                            <el-input v-model="formData.name" placeholder="请输入姓名" clearable prefix-icon="User" />
                        </el-form-item>
                    </el-col>

                    <el-col :xs="24" :sm="12" :md="14">
                        <el-form-item label="登录密码" prop="password">
                            <el-input type="password" v-model="formData.password" placeholder="请输入6-20位密码" show-password
                                clearable prefix-icon="Lock" />
                        </el-form-item>
                    </el-col>

                    <!-- 第二行 -->
                    <el-col :xs="24" :sm="12" :md="10">
                        <el-form-item label="电子邮箱" prop="email">
                            <el-input v-model="formData.email" placeholder="name@example.com" clearable
                                prefix-icon="Message" />
                        </el-form-item>
                    </el-col>

                    <el-col :xs="24" :sm="12" :md="14">
                        <el-form-item label="联系电话" prop="phone">
                            <el-input v-model="formData.phone" placeholder="13800138000" clearable
                                prefix-icon="Iphone" />
                        </el-form-item>
                    </el-col>

                    <!-- 第三行 -->
                    <el-col :xs="24" :sm="12" :md="10">
                        <el-form-item class="submit-button">
                            <el-button aria-label="提交" type="primary" @click="handleSubmit" :loading="isSubmitting" icon="Plus">
                                添加员工
                            </el-button>
                        </el-form-item>
                    </el-col>

                    <el-col :xs="24" :sm="12" :md="14">
                        <el-form-item label="职位角色" prop="role">
                            <el-radio-group v-model="formData.role">
                                <el-radio-button label="manager" value="manager">
                                    <el-icon>
                                        <User />
                                    </el-icon>
                                    业务员
                                </el-radio-button>
                                <el-radio-button label="admin" value="admin">
                                    <el-icon>
                                        <Setting />
                                    </el-icon>
                                    管理员
                                </el-radio-button>
                            </el-radio-group>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
        </el-card>

        <!-- 操作工具栏 -->
        <div class="action-toolbar">
            <div class="toolbar-left">
                <el-input v-model="searchKeyword" placeholder="输入姓名搜索..." clearable style="width: 260px"
                    @clear="handleSearch">
                    <template #append>
                        <el-button aria-label="提交" icon="Search" @click="handleSearch" />
                    </template>
                </el-input>
            </div>

            <div class="toolbar-right">
                <el-button aria-label="提交" type="danger" :disabled="selectedUser.length === 0" @click="handleBatchDelete" icon="Delete"
                    plain>
                    批量删除 ({{ selectedUser.length }})
                </el-button>
            </div>
        </div>

        <!-- 数据表格 -->
        <el-table :data="userList" style="width: 100%" border stripe @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column prop="id" label="ID" width="100" align="center" />
            <el-table-column prop="username" label="姓名" min-width="120" show-overflow-tooltip />
            <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />

            <el-table-column label="操作" width="200" fixed="right" align="center">
                <template #default="scope">
                    <el-button type="primary" size="small" icon="Edit" @click="editUser(scope.row)" />
                    <el-button type="danger" size="small" icon="Delete" @click="deleteUser(scope.row)" />
                </template>
            </el-table-column>
        </el-table>

        <!-- 编辑对话框 -->
        <el-dialog v-model="editDialogVisible" title="编辑员工信息" width="500px">
            <el-form :model="currentUser" label-width="80px">
                <el-form-item label="员工姓名">
                    <el-input v-model="currentUser.username" />
                </el-form-item>
                <el-form-item label="联系电话">
                    <el-input v-model="currentUser.mobile" />
                </el-form-item>
            </el-form>

            <template #footer>
                <el-button @click="editDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="confirmEdit">确认修改</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '@/services/apiClient'
import { ArrowRight } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/userStore'
import showConfirmDialog from '@/utils/showConfirmDialog'

const userStore = useUserStore();


// 员工数据
const userList = ref([])
interface User {
    id: number | string;
    username: string;
    [key: string]: any;
}
const selectedUser = ref<User[]>([])
const searchKeyword = ref('')
const editDialogVisible = ref(false)
const currentUser = ref({
    id: null,
    username: '',
    mobile: ''
})

// 初始化加载数据
onMounted(() => {
    fetchUserList()
})

// 获取员工列表
const fetchUserList = async () => {
    try {
        const response = await apiClient.get('get_user/')
        if (response.data.code === 1) {
            userList.value = response.data.data.map((user: any) => ({
                ...user,
            }))
        }
    } catch (error) {
        const errMsg = (error as any)?.response?.data?.msg || (error as any)?.message || '未知错误';
        ElMessage.error('获取员工列表失败: ' + errMsg)
    }
}

// 搜索员工
const handleSearch = async () => {
    try {
        const response = await apiClient.post('query_user/', {
            inputstr: searchKeyword.value
        })
        if (response.data.code === 1) {
            userList.value = response.data.data.map((user: { role: string }) => ({
                ...user,
                position: user.role === 'manager' ? '经理' : '管理员',
                department: '管理部门'
            }))
        }
    } catch (error) {
        const err = error as any;
        ElMessage.error('搜索失败: ' + (err.response?.data?.msg || err.message))
    }
}

// 删除
const deleteUser = async (row: { username: string; id: any }) => {
    // 检查是否尝试删除自己
    if (row.username === userStore.userInfo.name) {
        ElMessage.warning('您不能删除自己的账户');
        return; // 阻止后续操作
    }

    if (row.username === 'customer' || row.username === 'manager' || row.username === 'admin') {
        ElMessage.warning('测试用户不允许删除');
        return; // 阻止后续操作
    }

    try {
        await showConfirmDialog(`确认删除 ${row.username} 吗？`, '警告');

        const response = await apiClient.post('delete_user/', row.id); // 确保发送的数据格式正确
        if (response.data.code === 1) {
            ElMessage.success('删除成功');
            fetchUserList();
        } else {
            ElMessage.error('删除失败: ' + (response.data.msg || '未知错误'));
        }
    } catch (error: any) {
        if (error !== 'cancel') {
            ElMessage.error('删除失败: ' + (error.response?.data?.msg || error.message));
        }
    }
};

// 批量删除
const handleBatchDelete = async () => {
    const currentUserUsername = userStore.userInfo.name;
    if (selectedUser.value.some(user => user.username === currentUserUsername)) {
        ElMessage.warning('您不能删除自己的账户');
        return; // 阻止后续操作
    }

    if (selectedUser.value.some(user => user.username === 'customer' || user.username === 'manager' || user.username === 'admin')) {
        ElMessage.warning('测试用户不允许删除');
        return; // 阻止后续操作
    }

    try {
        await showConfirmDialog(`确认删除选中的 ${selectedUser.value.length} 位用户吗？`, '警告');
        const response = await apiClient.post('delete_users/', {
            users: selectedUser.value.map(user => (user.id))
        })

        if (response.data.code === 1) {
            ElMessage.success('批量删除成功')
            fetchUserList()
            selectedUser.value = []
        }
    } catch (error) {
        if (error !== 'cancel') {
            const err = error as any;
            ElMessage.error('删除失败: ' + (err.response?.data?.msg || err.message))
        }
    }
}

const editUser = (row: { id: null; username: string; mobile: string } | { id: null; username: string; mobile: string }) => {
    if (!row) {
        ElMessage.error('编辑失败: 未选择员工')
        return
    }
    currentUser.value = { ...row }
    editDialogVisible.value = true
}

const confirmEdit = async () => {
    if (currentUser.value.username === 'customer' || currentUser.value.username === 'manager' || currentUser.value.username === 'admin') {
        ElMessage.warning('测试用户不允许修改');
        return; // 阻止后续操作
    }

    try {
        if (!currentUser.value.id) {
            ElMessage.error('修改失败: 未选择员工')
            return
        }
        const response = await apiClient.post('update_user/', {
            id: currentUser.value.id,
            username: currentUser.value.username,
            mobile: currentUser.value.mobile
        })

        if (response.data.code === 1) {
            ElMessage.success('修改成功')
            editDialogVisible.value = false
            fetchUserList()
        } else {
            ElMessage.error('修改失败: ' + (response.data.msg || '未知错误'))
        }
    } catch (error) {
        const err = error as any;
        ElMessage.error('修改失败: ' + (err.response?.data?.msg || err.message))
    }
}
// 多选处理
const handleSelectionChange = (selection: never[]) => {
    selectedUser.value = selection
}


import type { FormInstance } from 'element-plus'
const formRef = ref<FormInstance | null>(null);
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
        // { type: 'email', message: '请输入有效的电子邮件', trigger: ['blur', 'change'] }
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
        if (!formRef.value) {
            ElMessage.error('表单未初始化');
            return;
        }
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
        fetchUserList()
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
