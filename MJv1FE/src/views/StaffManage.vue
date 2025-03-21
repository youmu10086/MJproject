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
    <el-table :data="staffList" style="width: 100%; overflow: visible" :size="size" border
        :row-class-name="tableRowClassName" max-height="420" table-layout="fixed">
        <el-table-column type="selection"></el-table-column>
        <el-table-column prop="name" label="姓名" min-width="80" align="center" show-overflow-tooltip />
        <el-table-column prop="position" label="职位" min-width="100" align="center" show-overflow-tooltip />
        <el-table-column prop="department" label="部门" min-width="100" align="center" show-overflow-tooltip />
        <el-table-column prop="email" label="邮箱" min-width="150" align="center" show-overflow-tooltip />
        <el-table-column prop="phone" label="电话" min-width="120" align="center" show-overflow-tooltip />

        <!-- 操作列 -->
        <el-table-column label="操作" min-width="240" align="center">
            <template v-slot="scope">
                <el-button plain :size="size" @click="viewStaff(scope.row)">查看</el-button>
                <el-button type="primary" :size="size" plain @click="editStaff(scope.row)">编辑</el-button>
                <el-button type="danger" :size="size" plain @click="deleteStaff(scope.row)">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
</template>

<script setup>
// 模拟的职工数据
const staffList = ref([
  { id: 1, name: '张三', position: '经理', department: '销售部', email: 'zhangsan@example.com', phone: '12345678901' },
  { id: 2, name: '李四', position: '主管', department: '技术部', email: 'lisi@example.com', phone: '12345678902' },
  { id: 3, name: '王五', position: '职员', department: '行政部', email: 'wangwu@example.com', phone: '12345678903' },
]);
 
// 表格大小
const size = ref('default');
 
// 表格行样式（此处未实际使用，可根据需要自定义）
const tableRowClassName = ({ row, rowIndex }) => {
  return '';
};
 
// 查看职工信息（具体实现省略）
const viewStaff = (row) => {
  console.log('查看职工:', row);
};
 
// 编辑职工信息（具体实现省略）
const editStaff = (row) => {
  console.log('编辑职工:', row);
};
 
// 删除职工信息（具体实现省略）
const deleteStaff = (row) => {
  console.log('删除职工:', row);
};



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