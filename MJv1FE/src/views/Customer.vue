<template>
    <div>
        <el-breadcrumb :separator-icon="ArrowRight" class="no-select">
            <el-breadcrumb-item to="/Home">首页</el-breadcrumb-item>
            <el-breadcrumb-item>入住人员管理</el-breadcrumb-item>
        </el-breadcrumb>
        <!----------------------------------------------------------------------------------- 顶部操作 ------------------------------------------------------------------------------------------->
        <el-form :inline="true" class="top-form" @submit.prevent=queryCustomer>
            <el-row>
                <el-col :span="18">
                    <el-input v-model="inputStr" placeholder="输入查询条件" clearable class="search-input"
                        :prefix-icon="Search" />
                </el-col>
                <el-col :span="6" class="button-group-container">
                    <el-button-group class="button-group">
                        <el-button type="primary" v-if="inputStrIsEmpty" :icon="Refresh" plain
                            @click="getCustomer()">刷新</el-button>
                        <el-button type="primary" v-else :icon="Search" plain @click="queryCustomer()">查询</el-button>

                        <el-button type="primary" :icon="Plus" plain @click="addCustomer()">现场入住</el-button>
                    </el-button-group>
                </el-col>
            </el-row>
        </el-form>
        <!------------------------------------------------------------------------------------ 表 -------------------------------------------------------------------------------------------->
        <base-table :table-data="currentPageTableData" :columns="columns" :size="size"
            :row-class-name="tableRowClassName" :default-sort="{ prop: 'roomNo', order: 'descending' }"
            :max-height="400" show-selection @selection-change="handleSelectionChange">
            <!-- 自定义列：住宿时间 -->
            <template #resideTimePeriod="{ scope }">
                {{ formatResideTime(scope.row.resideTimePeriod[0], scope.row.resideTimePeriod[1]) }}
            </template>

            <!-- 自定义操作列 -->
            <template #actions="{ scope }">
                <div class="button-group">
                    <el-button v-if="scope.row.status === '已入住'" plain :size="size"
                        @click="renewal(scope.row)">续租</el-button>
                    <el-button v-if="scope.row.status === '已入住'" plain :size="size"
                        @click="checkOut(scope.row)">退宿</el-button>
                    <el-button v-if="scope.row.status === '已预订'" plain :size="size"
                        @click="checkInForServed(scope.row)">预订顾客入住</el-button>
                    <el-button v-if="scope.row.status === '已退宿'" plain :size="size" disabled>该顾客已退宿</el-button>
                    <el-button v-if="scope.row.status === '已取消预订'" plain :size="size" disabled>该顾客取消预订</el-button>

                    <el-button type="primary" :size="size" :icon="Edit" circle plain
                        @click="updateCustomer(scope.row)" />
                    <el-button type="success" :size="size" :icon="More" circle plain @click="viewCustomer(scope.row)" />
                    <el-button type="danger" :size="size" :icon="Delete" circle plain
                        @click="deleteCustomer(scope.row)" />
                </div>
            </template>
        </base-table>
        <!--------------------------------------------------------------------------------- 底部操作 ------------------------------------------------------>
        <el-row style="margin-top: 10px;">
            <el-col :span="8" style="text-align: left;">
                <el-button type="primary" :icon="Delete" plain @click="deleteCustomers">批量删除</el-button>
            </el-col>
            <el-col :span="16" style="text-align: right;">
                <div style="display: inline-block;">
                    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                        v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[5, 10, 20, 50]"
                        :size="size" layout="total, sizes, prev, pager, next, jumper" :total="total" />
                </div>
            </el-col>
        </el-row>
        <!-------------------------------------------------------------------- 表单 ------------------------------------------------------------------>
        <CustomerMessageForm v-model:visible="customerDialogVisible" :title="customerDialogTitle"
            v-model:customerForm="customerForm" :rules="rules" :customer-dialog-status="customerDialogStatus"
            :loading="isSubmitting" :submitRemand="submitRemand" :size="size" @submit="submitForm"
            @before-close="handleClose" @resetForm="resetForm" @close="closeCustomerDialog" @room-message="roomMessage"
            @upload-picture-post="uploadPicturePost" @before-avatar-upload="beforeAvatarUpload"
            @close-customer-dialog-form="closedCustomerDialog" />
    </div>
</template>

<script lang="ts" setup>
defineOptions({ name: 'CustomerPage' });
import BaseTable from '@/components/BaseTable.vue';
import CustomerMessageForm from '@/components/CustomerMessageForm.vue';
import showConfirmDialog from '@/utils/showConfirmDialog';
import { computed, onMounted, ref } from 'vue'
import { ArrowRight, Delete, Edit, More, Plus, Refresh, Search } from '@element-plus/icons-vue'
import { ComponentSize, dayjs, ElMessage, FormInstance, FormItemRule, UploadProps } from 'element-plus'
import apiClient from '@/services/apiClient';
import { AxiosResponse } from 'axios';
import { Room } from '@/types/Room'; // 引入Room类型
import { Customer, CustomerDialogStatus, CustomerInterface } from '@/types/Customer'; // 引入Customer类型
import { formatResideTime, processResideTimePeriod } from '@/utils/dateUtils'; // 引入工具函数
import { RoomInterface } from '@/types/Room';

const columns = [
    { prop: 'name', label: '姓名', minWidth: 50, showOverflowTooltip: true },
    { prop: 'roomNo', label: '房间号', minWidth: 80, sortable: true },
    { prop: 'balance', label: '余额', minWidth: 70, showOverflowTooltip: true },
    { prop: 'status', label: '状态', minWidth: 70, showOverflowTooltip: true },
    { prop: 'resideTimePeriod', label: '住宿时间', minWidth: 260, showOverflowTooltip: true },
    { prop: 'idCardNo', label: '身份证', minWidth: 150, showOverflowTooltip: true },
    { prop: 'mobile', label: '电话号码', minWidth: 100, showOverflowTooltip: true },
];

const isSubmitting = ref(false); // 控制按钮的加载状态
const roomMessage = (roomNo: string) => {
    const roomInfo = roomData.value.find(room => room.room_no === roomNo) || null;
    if (roomNo === '' || roomInfo === null)
        return '';
    else {
        const roomAmount = roomInfo ? roomInfo.roomAmount || '未知' : '未找到房间';
        return `单价${roomAmount})`;
    }
}

const deposit = 100;//押金

// 退租
const checkOut = (row: Customer) => {
    const startDate = new Date(row.resideTimePeriod[0]);
    const endDate = new Date(row.resideTimePeriod[1]);

    let timeDifference: number = endDate.getTime() - startDate.getTime();
    const info = roomData.value.find(room => room.room_no === row.roomNo);
    let minimumAmount: number = 0;
    if (info) {
        if (info.durationType === "日租") {
            timeDifference = timeDifference / 86400000; // 转换为天数
            minimumAmount = timeDifference * info.roomAmount;
        } else if (info.durationType === "钟点房") {
            timeDifference = timeDifference / 3600000; // 转换为小时数  
            minimumAmount = timeDifference * info.roomAmount;
        } else if (info.durationType === "月租") {
            timeDifference = timeDifference / 2629746000; // 转换为月份                         
            minimumAmount = timeDifference * info.roomAmount;
        }
    }
    if (row.balance === null) return;
    showConfirmDialog('确定为顾客' + row.name + '退宿吗？(若退宿请返还押金' + deposit + '元、充值剩余' + (row.balance - minimumAmount) + '元)', '警告')
        .then(() => {
            customerForm.value = JSON.parse(JSON.stringify(row));
            customerForm.value.image = getImage(row.cno);
            customerForm.value.imageUrl = apiClient.defaults.baseURL + 'media/' + customerForm.value.image;
            customerForm.value.checkOutTime = new Date();
            customerForm.value.balance = 0;
            customerForm.value.status = '已退宿';

            submitUpdateCustomer()
                .then(() => ElMessage.success('退租成功'))
                .catch(() => ElMessage.error('退租失败'));
        })
        .catch(() => {
            ElMessage.info('取消退租');
        });
}
// 续租
const oldResideTimePeriod = ref<string[]>([]);
const renewal = (row: Customer) => {
    oldResideTimePeriod.value = row.resideTimePeriod;
    initializeCustomerForm(row, { resideTimePeriod: ['', ''] }); // 清空居住时间
    customerDialogStatus.value = CustomerDialogStatus.RENEWAL;
    customerDialogVisible.value = true;
};
// 预订顾客办理入住
const checkInForServed = (row: Customer) => {
    initializeCustomerForm(row, {
        checkInTime: new Date(),
        status: '已入住',
    }); // 设置入住时间和状态
    customerDialogStatus.value = CustomerDialogStatus.CHECKINFORSERVED;
    customerDialogVisible.value = true;
};
const initializeCustomerForm = (row: Customer, overrides: Partial<Customer> = {}) => {
    // 深拷贝 row 数据到 customerForm
    customerForm.value = { ...JSON.parse(JSON.stringify(row)) };

    // 获取图片并拼接 URL
    customerForm.value.image = getImage(row.cno);
    customerForm.value.imageUrl = `${apiClient.defaults.baseURL}media/${customerForm.value.image}`;

    // 应用 overrides 参数覆盖指定字段
    Object.assign(customerForm.value, overrides);
};

const size = ref<ComponentSize>('small')                           // 组件大小
const customerDate = ref<Customer[]>([])                              // 储存请求信息
const roomData = ref<Room[]>([])

const currentPageTableData = ref<Customer[]>([])                   // 当前展示的信息
const inputStr = ref('')
const inputStrIsEmpty = computed(() => {
    return inputStr.value === ''
})
const customerDialogTitle = computed(() => {
    if (customerDialogStatus.value === CustomerDialogStatus.ADD)
        return '现场入住'
    else if (customerDialogStatus.value === CustomerDialogStatus.EDIT)
        return '修改信息'
    else if (customerDialogStatus.value === CustomerDialogStatus.VIEW)
        return '查看明细'
    else if (customerDialogStatus.value === CustomerDialogStatus.RENEWAL)
        return '续租'
    else if (customerDialogStatus.value === CustomerDialogStatus.CHECKINFORSERVED)
        return '预订顾客办理入住'
    else
        return ''
})
const customerDialogStatus = ref<CustomerDialogStatus>(CustomerDialogStatus.NONE)  // 对话框状态
const rules = ref({
    name: [
        { required: true, message: '姓名不能为空', trigger: 'blur' }
    ] as Array<FormItemRule>,
    roomNo: [
        { required: true, message: '房间号不能为空', trigger: 'blur', },
        {
            validator: (_, value, callback) => {
                const exists = roomData.value.some(room => room.room_no === value);
                if (!exists)
                    return callback(new Error('没有这个房间'));
                callback(); // 验证通过
            }, trigger: 'blur'
        },
        {
            validator: (_, value, callback) => {
                const room = roomData.value.find(room => room.room_no === value);
                if (!room)
                    return callback(new Error('没有这个房间'));
                if (room.roomStatus === 'reserved' && customerDialogStatus.value === CustomerDialogStatus.CHECKINFORSERVED && customerForm.value.roomNo === value)
                    return callback(); // 预约用户入住时跳过验证
                else if (room.roomStatus === 'occupied' && customerDialogStatus.value === CustomerDialogStatus.RENEWAL && customerForm.value.roomNo === value)
                    return callback(); // 入住用户续租时跳过验证
                else if (room.roomStatus !== 'vacant')
                    return callback(new Error('该房间已被占用'));
                callback(); // 验证通过
            }, trigger: 'blur'
        }
    ] as Array<FormItemRule>,
    idCardNo: [
        { required: true, message: '身份证号不能为空', trigger: 'blur' }
    ] as Array<FormItemRule>,
    mobile: [
        { required: true, message: '手机号不能为空', trigger: 'blur' }
    ] as Array<FormItemRule>,
    resideTimePeriod: [
        { required: true, message: '时间不能为空', trigger: 'blur' },
        {
            validator: (_, value, callback) => {
                if (value[0] === '' || value === '')
                    callback(new Error('时间不能为空')); // 跳过验证  
                else
                    callback(); // 验证通过
            },
            trigger: 'blur'
        },
        {
            validator: (_, value, callback) => {
                if (customerDialogStatus.value !== CustomerDialogStatus.RENEWAL) {
                    callback(); // 跳过验证  
                } else {
                    const oldStartDate = new Date(oldResideTimePeriod.value[0]);
                    const oldEndDate = new Date(oldResideTimePeriod.value[1]);
                    const startDate = new Date(customerForm.value.resideTimePeriod[0]);
                    const endDate = new Date(customerForm.value.resideTimePeriod[1]);
                    const formattedStartDate = dayjs(oldStartDate).format('YYYY年MM月DD日HH时');
                    const formattedEndDate = dayjs(oldEndDate).format('YYYY年MM月DD日HH时');
                    if (oldStartDate.getTime() != startDate.getTime())
                        return callback(new Error('开始时间需与原时间' + formattedStartDate + '一致'));
                    if (oldEndDate.getTime() >= endDate.getTime())
                        return callback(new Error('续租时间需超过原退房时间' + formattedEndDate));
                    callback(); // 验证通过
                }
            },
            trigger: 'blur'
        }
    ] as Array<FormItemRule>,
    balance: [
        { required: true, message: '余额不能为空', trigger: 'blur' },
        {
            validator: (_, value, callback) => {
                const startDate = new Date(customerForm.value.resideTimePeriod[0]);
                const endDate = new Date(customerForm.value.resideTimePeriod[1]);

                let timeDifference: number = endDate.getTime() - startDate.getTime();
                const info = roomData.value.find(room => room.room_no === customerForm.value.roomNo);

                if (info) {
                    if (info.durationType === "日租") {
                        timeDifference = timeDifference / 86400000; // 转换为天数
                        const minimumAmount = timeDifference * info.roomAmount + deposit;
                        if (value < minimumAmount) {
                            return callback(new Error('充值金额至少为' + minimumAmount + '元'));
                        }
                    } else if (info.durationType === "钟点房") {
                        timeDifference = timeDifference / 3600000; // 转换为小时数  
                        const minimumAmount = timeDifference * info.roomAmount + deposit;
                        if (value < timeDifference * info.roomAmount) {
                            return callback(new Error('充值金额至少为' + minimumAmount + '元'));
                        }
                    } else if (info.durationType === "月租") {
                        timeDifference = timeDifference / 2629746000; // 转换为月份                         
                        const minimumAmount = timeDifference * info.roomAmount + deposit;
                        if (value < timeDifference * info.roomAmount) {
                            return callback(new Error('充值金额至少为' + minimumAmount + '元'));
                        }
                    }
                }
                callback(); // 验证通过  
            },
            trigger: 'blur'
        }
    ] as Array<FormItemRule>,
});
const customerForm = ref<Customer>({
    cno: '',
    name: '',
    roomNo: '',
    gender: '男',
    checkInTime: null,// 登记时间    
    checkOutTime: null,// 退房时间
    idCardNo: '',
    mobile: '',
    image: '',
    imageUrl: '',
    balance: 0,
    resideTimePeriod: ['', ''],
    status: '',
});
// ————————————————————————————————————————————————————————————————————————————————————页面控制———————————————————————————————————————————————————————————————————————————————— //
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(1)                                           // 总行数
const currentpage = ref(1)                                     // 当前页数
const pagesize = ref(10)                                        // 每页行数
// 分页时修改每页都行数
const handleSizeChange = (size: number) => {
    pagesize.value = size;
    getPageCustomer();
}
// 调整当前的页码
const handleCurrentChange = (pageNumber: number) => {
    currentpage.value = pageNumber;
    getPageCustomer();
}
// 退出对话框时询问
const handleClose = (done: () => void) => {
    if (customerDialogStatus.value === CustomerDialogStatus.VIEW) done()
    else {
        showConfirmDialog('信息还未保存，确定退出吗？', '警告')
            .then(() => { done() })
            .catch(() => { })
    }
}
// 根据截至时间改变列的颜色
const tableRowClassName = (row: Record<string, unknown>) => {
    // 防御性检查
    if (!row.resideTimePeriod || !Array.isArray(row.resideTimePeriod) || row.resideTimePeriod.length < 2) {
        return ''; // 返回默认样式
    }

    try {
        const now = dayjs();
        const endDate = dayjs((row.resideTimePeriod as [string, string])[1], undefined, true);

        // 检查日期是否有效
        if (!endDate.isValid()) {
            return '';
        }

        if (row.status === '已退宿') return '';
        else if (endDate.isBefore(now)) return 'danger-row'; // 过期
        else if (endDate.isAfter(now.add(1, 'day'))) return 'success-row'; // 正常
        else return 'warning-row'; // 即将到期
    } catch (error) {
        console.error('日期处理错误:', error);
        return ''; // 出错时返回默认样式
    }
}
// 根据页面设置加载当前页顾客的信息
const getPageCustomer = () => {
    currentPageTableData.value = [];
    for (let i = (currentpage.value - 1) * pagesize.value; i < total.value; i++) {
        currentPageTableData.value.push(customerDate.value[i]);
        if (currentPageTableData.value.length === pagesize.value) break;
    }
}
// 开始时请求表的数据
onMounted(() => {
    getCustomer();
    getRoom();
})

// ————————————————————————————————————————————————————————————————————————————————————————————操作—————————————————————————————————————————————————————————————————————————————————— //
const customerDialogVisible = ref(false) // 显示dialog
// 获取所有房客信息
const getCustomer = async () => {
    try {
        inputStr.value = '';
        const response = await apiClient.get("customer/");
        if (response.data.code === 1) {
            flushedDate(response);
        }
    } catch {/* empty */ }
};
// 根据返回值重新加载页面（customerDate和total.value赋值）
const flushedDate = (res: AxiosResponse<unknown>) => {
    const data = res.data as { data: CustomerInterface[] };
    customerDate.value = data.data.map((item: CustomerInterface) => ({
        ...item,
        image: item.image || '', // 确保 image 字段存在
        imageUrl: item.image ? `${apiClient.defaults.baseURL}media/${item.image}` : '', // 拼接图片 URL
        resideTimePeriod: processResideTimePeriod(item.resideTimePeriod), // 自定义处理函数
    }));
    total.value = data.data.length;
    getPageCustomer();
}
const getRoom = async () => {
    try {
        const res = await apiClient.get("room/");
        if (res.data.code === 1) {
            // 解析后端返回的数据
            roomData.value = res.data.data.map((room: RoomInterface) => ({
                roomNo: room.room_no,
                roomStatus: room.room_status,
                roomType: room.room_type,
                roomAmount: room.room_amount,
                durationType: room.duration_type,
                roomConfig: room.room_config || [], // 确保 roomConfig 存在
            }));
        }
    } finally { /* empty */ }
};
// 显示查看明细对话框
const viewCustomer = (row: Customer) => {
    initializeCustomerForm(row); // 不需要额外覆盖字段
    customerDialogStatus.value = CustomerDialogStatus.VIEW;
    customerDialogVisible.value = true;
};
// 显示修改信息对话框
const updateCustomer = (row: Customer) => {
    initializeCustomerForm(row); // 调用封装的函数
    customerDialogStatus.value = CustomerDialogStatus.EDIT;
    customerDialogVisible.value = true;
};
// 显示添加对话框
const addCustomer = () => {
    customerDialogStatus.value = CustomerDialogStatus.ADD;
    customerDialogVisible.value = true;
}
// 重置CustomerForm
const resetCustomerForm = () => {
    customerForm.value.checkOutTime = null;
    customerForm.value.gender = '男';
    customerForm.value.idCardNo = '';
    customerForm.value.mobile = '';
    customerForm.value.name = '';
    customerForm.value.checkInTime = null;
    customerForm.value.roomNo = '';
    customerForm.value.image = '';
    customerForm.value.imageUrl = '';
    customerForm.value.balance = 0;
    customerForm.value.resideTimePeriod = ['', ''];
    customerDialogStatus.value = CustomerDialogStatus.NONE;
}
const closeCustomerDialog = () => {
    customerDialogVisible.value = false;
}
// 关闭对话框重置customerForm
const closedCustomerDialog = () => {
    resetCustomerForm();
}
const submitRemand = computed(() => {
    if (customerDialogStatus.value === CustomerDialogStatus.ADD)
        return '提交'
    else if (customerDialogStatus.value === CustomerDialogStatus.EDIT)
        return '修改'
    else if (customerDialogStatus.value === CustomerDialogStatus.RENEWAL)
        return '续租'
    else if (customerDialogStatus.value === CustomerDialogStatus.CHECKINFORSERVED)
        return '办理入住'
    else if (customerDialogStatus.value === CustomerDialogStatus.VIEW)
        return '确定'
    else
        return ''
})
// 重置表单验证状态
const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    formEl.clearValidate();
}
// 校验
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    isSubmitting.value = true;
    try {
        await formEl.validate((valid) => {
            if (valid) {
                if (customerDialogStatus.value === CustomerDialogStatus.ADD) submitAddCustomer();
                else submitUpdateCustomer();
            }
        });
    } finally {
        isSubmitting.value = false;
    }
};
// 查询
const queryCustomer = async () => {
    try {
        const response = await apiClient.post('customer/query/', { inputstr: inputStr.value });
        if (response.data.code === 1) {
            flushedDate(response);
            ElMessage.success('查询成功');
        }
    } catch { /*sb8*/ }
};
// 提交修改
const submitUpdateCustomer = async () => {
    try {
        const response = await apiClient.post("customer/update/", customerForm.value);
        if (response.data.code === 1) {
            flushedDate(response);
            ElMessage.success('修改成功');
            closeCustomerDialog();
            closedCustomerDialog();
        } else {
            ElMessage.error('修改失败');
        }
    } catch { /*empty*/ }
};
// 提交添加
const submitAddCustomer = async () => {
    customerForm.value.checkInTime = new Date();
    customerForm.value.status = '已入住';
    try {
        const response = await apiClient.post("customer/add/", customerForm.value);
        if (response.data.code === 1) {
            flushedDate(response);
            ElMessage.success('办理入住成功')
            closeCustomerDialog();
            closedCustomerDialog();
        }
    } catch { /* empty */ }
};
// 删除
const deleteCustomer = async (row: { name: string; cno: string }) => {
    try {
        // 显示确认对话框，并等待用户确认
        await showConfirmDialog(
            `是否永久删除姓名为 ${row.name} 的顾客信息?`,
            '警告'
        );

        // 发送删除请求，并等待响应
        const response = await apiClient.post("customer/delete/", row.cno);

        // 检查响应状态
        if (response.data.code === 1) {
            flushedDate(response);
            ElMessage.success('删除成功');
            closeCustomerDialog();
            closedCustomerDialog();
        }
    } catch { /* empty */ }
};
// 批量删除
const selectCustomers = ref<Customer[]>([])
const handleSelectionChange = (data: Customer[]) => {
    selectCustomers.value = data
}
const deleteCustomers = async () => {
    try {
        await showConfirmDialog('是否批量删除' + selectCustomers.value.length + '个顾客的信息?', '警告')
        const response = await apiClient.post("customers/delete/", { customers: selectCustomers.value })
        if (response.data.code === 1) {
            flushedDate(response);
            ElMessage.success('批量删除成功')
            closeCustomerDialog();
            closedCustomerDialog();
        }
    } catch { /* empty */ }
}
// 判断图片类型
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
    if (rawFile.type !== 'image/jpeg') {
        ElMessage.error('必须为JPG格式')
        return false
    } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('大小不超过2MB')
        return false
    }
    return true
}
// 上传文件
const uploadPicturePost = async (file: { file: string | Blob; }) => {
    try {
        // 创建 FormData 对象
        const fileReq = new FormData();
        fileReq.append('avatar', file.file);

        // 发送 POST 请求
        const res = await apiClient.post('upload/', fileReq);

        // 处理响应
        if (res.data.code === 1) {
            customerForm.value.image = res.data.name;
            // 拼接全称
            customerForm.value.imageUrl = apiClient.defaults.baseURL + 'media/' + res.data.name;
            return res;  // 返回结果以便于后续处理
        } else throw new Error(res.data.msg); // 抛出错误以便于后续处理
    } catch { /* 错误处理 */ }
};
// 根据id获取image
const getImage = (cno: string) => {
    for (let oneCustomer of customerDate.value) {
        if (oneCustomer.cno === cno) {
            return oneCustomer.image;
        }
    }
    return '';
}
</script>
