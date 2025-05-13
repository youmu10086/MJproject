<template>
    <el-breadcrumb :separator-icon="ArrowRight" class="no-select mb-4">
        <el-breadcrumb-item to="/Home">首页</el-breadcrumb-item>
        <el-breadcrumb-item>公寓房间管理</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="container" :class="{ dark: isDark }">
        <el-skeleton :rows="5" animated v-if="loading" />
        <el-empty v-else-if="!hasRooms" description="暂无房间数据" />
        <template v-else>
            <!-- 所有房间 -->
            <el-card shadow="never" class="floor-card">
                <template #header>
                    <div class="floor-header">
                        <span class="floor-title">当前楼层：{{ currentFloor.title }}</span>
                        <el-button-group>
                            <el-button aria-label="提交" v-for="floor in floors" :key="floor.name"
                                :type="floor.name === currentFloor.name ? 'primary' : 'default'"
                                @click="switchFloor(floor)">
                                {{ floor.title }}
                            </el-button>
                        </el-button-group>
                        <el-button-group class="right-aligned">
                            <el-button v-if="isManager" @click="openAddRoomDialog">添加房间</el-button>
                            <el-button v-if="isManager">添加楼层</el-button>
                        </el-button-group>
                    </div>
                </template>

                <el-row v-if="getFloorRooms(currentFloor.name).length" :gutter="12">
                    <el-col v-for="room in getFloorRooms(currentFloor.name)" :key="room.roomNo || Math.random()"
                        :xs="12" :sm="8" :md="6" :lg="4" :xl="8" class="room-col">
                        <el-button class="room-button" :type="getRoomStatus(room).type" :size="size"
                            @click="openRoomDialog(room)" :plain="true">
                            <div class="room-info">
                                <span class="room-number">{{ room.roomNo || '未知房间号' }}</span>
                                <el-tag v-if="getRoomStatus(room).status" :type="getRoomStatus(room).type" size="small"
                                    class="mt-1">
                                    {{ getRoomStatus(room).status }}
                                </el-tag>
                            </div>
                        </el-button>
                    </el-col>
                </el-row>
                <el-empty v-else description="暂无房间数据" />
            </el-card>
        </template>
    </div>
    <el-dialog v-model="roomDialogVisible" :title="roomDialogTitle" width="900px" :close-on-click-modal="false"
        @closed="resetRoomForm">
        <template #header>
            <div style="display: flex; align-items: center;">
                <span>{{ roomDialogTitle }}</span>
                <el-input v-if="roomFormStatus === 'isAdding'" v-model="roomForm.roomNo" placeholder="请输入房间号"
                    size="small" style="margin-left: 10px; width: 100px;" />
            </div>
        </template>
        <el-form :model="roomForm" :rules="roomFormRules" ref="formRef" label-width="120px" label-position="right"
            class="optimized-form">
            <div class="form-section">
                <el-row :gutter="30">
                    <el-col :xs="24" :sm="12" :md="8">
                        <el-form-item label="房间状态" prop="roomStatus">
                            <el-select v-model="roomForm.roomStatus" placeholder="请选择" class="full-width"
                                :disabled="!isManager">
                                <el-option v-for="(status, key) in roomStatusOptions" :key="key" :label="status.label"
                                    :value="key" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="12" :md="8">
                        <el-form-item label="房间类型" prop="roomType">
                            <el-input v-model="roomForm.roomType" placeholder="请输入类型" clearable class="full-width"
                                :disabled="!isManager" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="12" :md="8">
                        <el-form-item label="时间单位" prop="durationType">
                            <el-select v-model="roomForm.durationType" placeholder="请选择时间单位" class="full-width"
                                :disabled="!isManager">
                                <el-option label="钟点房" value="hourly" />
                                <el-option label="日租" value="daily" />
                                <el-option label="月租" value="monthly" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </div>
            <div class="form-section">
                <el-row :gutter="30">
                    <el-col :span="8">
                        <el-form-item label="房间金额" prop="roomAmount">
                            <el-input v-model="roomForm.roomAmount" placeholder="0.00" type="number"
                                class="amount-input" :disabled="!isManager">
                                <template #append>元</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="16">
                        <el-form-item label="房间配置">
                            <div class="config-tag-group">
                                <el-select v-model="roomForm.roomConfig" multiple placeholder="添加配置"
                                    class="add-config-tag" @change="addFormRoomConfig" :disabled="!isManager">
                                    <el-option v-for="config in allRoomConfigs" :key="config.id" :label="config.name"
                                        :value="config.name" />
                                    <template #footer>
                                        <el-button v-if="!isAddRoomConfig && !isDeleteRoomConfig" text bg size="small"
                                            @click="isAddRoomConfig = true">
                                            添加配置
                                        </el-button>
                                        <template v-if="isAddRoomConfig">
                                            <el-input v-model="newConfigName" class="option-input"
                                                placeholder="输入需要添加的配置名称" size="small"
                                                :loading="roomConfigSubmitting" />
                                            <el-button type="primary" size="small" @click="addRoomConfig">
                                                {{ roomConfigSubmitting ? '添加中...' : '确认添加' }}
                                            </el-button>
                                            <el-button size="small" @click="clear">取消</el-button>
                                        </template>
                                        <el-button v-if="!isAddRoomConfig && !isDeleteRoomConfig" text bg size="small"
                                            @click="isDeleteRoomConfig = true;">
                                            删除配置
                                        </el-button>
                                        <template v-if="isDeleteRoomConfig">
                                            <el-input v-model="newConfigName" class="option-input"
                                                placeholder="输入需要删除的配置名称" size="small" />
                                            <el-button type="primary" size="small" @click="deleteRoomConfig"
                                                :loading="roomConfigSubmitting">
                                                {{ roomConfigSubmitting ? '删除中...' : '确认删除' }}
                                            </el-button>
                                            <el-button size="small" @click="clear">取消</el-button>
                                        </template>
                                    </template>
                                </el-select>
                            </div>
                        </el-form-item>
                    </el-col>
                </el-row>
            </div>
            <div class="form-section">
                <el-form-item>
                    <el-upload action="#" list-type="picture-card" :on-preview="handlePreview" :on-remove="handleRemove"
                        :limit="5" class="image-uploader">
                        <i class="el-icon-plus"></i>
                    </el-upload>
                </el-form-item>
            </div>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="roomDialogVisible = false" size="small">取消</el-button>
                <el-button v-if="isManager" type="primary" @click="submitRoomForm" size="small"
                    :loading="RoomFormSubmitting">
                    {{ RoomFormSubmitting ? '提交中...' : '确认' }}
                </el-button>
                <el-button v-if="isCustomer" type="primary" @click="submitRoomForm" size="small"
                    :loading="RoomFormSubmitting">
                    {{ RoomFormSubmitting ? '提交中...' : '预订' }}
                </el-button>
            </div>
        </template>
    </el-dialog>

    <el-dialog v-model="customerDialogVisible" title='登记信息' style="width: 50%" :before-close="handleClose" draggable
        @closed="closeCustomerDialogForm" top="150px">
        <el-form :inline="true" label-width="110px" label-position="right" :model="customerForm" :rules="rules"
            ref="ruleFormRef">
            <el-row style="display: flex; align-items: center;">
                <el-col :span="12" style="padding-right: 5px;">
                    <el-form-item label="姓名" prop="name">
                        <el-input style="width: 100%;" v-model="customerForm.name" :size="size"></el-input>
                    </el-form-item>
                    <el-form-item label="身份号" prop="idCardNo">
                        <el-input style="width: 100%;" v-model="customerForm.idCardNo" :size="size"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12" style="padding-right: 5px;"> <!-- 证件照部分 -->
                    <el-form-item label="证件照">
                        <el-upload class="avatar-uploader" :action="customerForm.imageUrl" :show-file-list="false"
                            :before-upload="beforeAvatarUpload" style="text-align: center;" :size="size"
                            :http-request="uploadPicturePost">
                            <img v-if="customerForm.image" :src="customerForm.imageUrl" class="avatar" />
                            <el-icon v-else class="avatar-uploader-icon">
                                <Plus />
                            </el-icon>
                        </el-upload>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="10">
                <el-col :span="12" style="padding-right: 5px;">
                    <el-form-item label="电话" prop="mobile">
                        <el-input v-model="customerForm.mobile" :size="size"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="10" style="padding-left: 5px;">
                    <el-form-item label="房间号" prop="roomNo">
                        <el-input v-model="customerForm.roomNo" :size="size" disabled></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="6" style="padding-left: 5px;padding-top: 5px;">
                    <el-text style="width: 100%" :size="size">{{ roomMessage(customerForm.roomNo)
                        }}</el-text>
                </el-col>
                <el-col :span="8" style="padding-left: 5px;">
                    <el-form-item label="性别" prop="gender" label-width="40px">
                        <el-radio-group v-model="customerForm.gender" :size="size" style="width: 185px;" fill="#909399">
                            <el-radio-button value="男">男</el-radio-button>
                            <el-radio-button value="女">女</el-radio-button>
                        </el-radio-group>
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row>
                <el-col :span="18" style="padding-left: 5px;">
                    <el-form-item label="入住时间" prop="resideTimePeriod">
                        <el-date-picker type="datetimerange" v-model="customerForm.resideTimePeriod" style="width: 100%"
                            :size="size" unlink-panels range-separator="-" format="YYYY-MM-DD HH:mm:ss"
                            start-placeholder="开始" end-placeholder="结束" placement="top-start" />
                    </el-form-item>
                </el-col>
                <el-col :span="6" style="padding-left: 5px;padding-top: 5px;">
                    <el-text style="width: 100%" :size="size">{{ timeDifference(customerForm.resideTimePeriod)
                        }}</el-text>
                </el-col>
            </el-row>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button type="primary" @click="submitForm(ruleFormRef)"
                    :loading="customerFormisSubmitting">预订</el-button>
                <el-button type="info" @click="customerDialogVisible = false">取消</el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { ElMessage, ElUpload, UploadProps, FormInstance, FormItemRule } from 'element-plus';
import { ArrowRight } from '@element-plus/icons-vue';
import { ComponentSize } from 'element-plus';
import { onMounted, ref, computed } from 'vue';
import apiClient from '@/services/apiClient';
import { useDark } from '@vueuse/core';
import { useUserStore } from '@/store/userStore';
import { Plus } from '@element-plus/icons-vue';
import showConfirmDialog from '@/utils/showConfirmDialog';

const customerFormisSubmitting = ref(false); // 提交状态

const submitForm = async (formEl: FormInstance | undefined) => {
    customerFormisSubmitting.value = true; // 提交中状态
    // 检查表单必填项
    if (!customerForm.value.name || !customerForm.value.idCardNo || !customerForm.value.mobile) {
        ElMessage.error('请填写完整的登记信息');
        customerFormisSubmitting.value = false; // 提交取消，重置状态
        return;
    }

    try {
        await showConfirmDialog('请缴纳50元定金以继续预订', '缴纳定金');

        const now = new Date();
        customerForm.value.checkInTime = now;
        customerForm.value.status = '已预订'; // 设置状态为已预订
        customerForm.value.balance = 0; // 余额设置为0
        customerForm.value.user_id = userStore.userInfo.id; // 设置用户ID
        const response = await apiClient.post("customer/reserve/", customerForm.value);
        if (response.data.code === 1) {
            ElMessage.success('房间预订成功');
            getRoom();
        } else {
            ElMessage.error(response.data.msg || '房间预订失败');
        }
    } catch (error) {
    } finally {
        customerFormisSubmitting.value = false; // 无论请求成功还是失败，都重置提交状态
        customerDialogVisible.value = false; // 关闭弹窗
    }
};

const reservedRoom = async () => {
    try {
        RoomFormSubmitting.value = true; // 提交中状态
        customerForm.value.roomNo = roomForm.value.roomNo; // 设置房间号
        customerDialogVisible.value = true; // 打开登记信息弹窗
    } catch (error) { }
    finally {
        RoomFormSubmitting.value = false; // 提交完成状态
        roomDialogVisible.value = false; // 关闭房间信息弹窗
    }
};
const ruleFormRef = ref<FormInstance>()

// 返回时间差
const timeDifference = (times: string[]) => {
    if (times[0] === '' || times[1] === '')
        return '';
    else {
        const endDate = new Date(times[1]);
        const startDate = new Date(times[0]);

        // 计算时间差（毫秒）  
        const diffTime = endDate.getTime() - startDate.getTime();

        // 计算年、月、日、小时  
        const diffSeconds = Math.floor(diffTime / 1000);
        const diffMinutes = Math.floor(diffSeconds / 60);
        const diffHours = Math.floor(diffMinutes / 60);
        const diffDays = Math.floor(diffHours / 24);

        // 计算年和月  
        const years = Math.floor(diffDays / 365);
        const months = Math.floor((diffDays % 365) / 30);
        const days = diffDays % 30;
        const hours = diffHours % 24;

        return `${years}年${months}月${days}日${hours}小时`
    }
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
    } catch (err) { }
};
const roomMessage = (roomNo: string) => {
    const roomInfo = roomData.value.find(room => room.roomNo === roomNo) || null;
    if (roomNo === '' || roomInfo === null)
        return '';
    else {
        const roomAmount = roomInfo ? roomInfo.roomAmount || '未知' : '未找到房间';
        return `单价${roomAmount})`;
    }
}
const rules = ref({
    name: [
        { required: true, message: '姓名不能为空', trigger: 'blur' }
    ] as Array<FormItemRule>,
    roomNo: [
        { required: true, message: '房间号不能为空', trigger: 'blur', },
        {
            validator: (rule, value, callback) => {
                const exists = roomData.value.some(room => room.roomNo === value);
                if (!exists)
                    return callback(new Error('没有这个房间'));
                callback(); // 验证通过
            }, trigger: 'blur'
        },
        {
            validator: (rule, value, callback) => {
                const room = roomData.value.find(room => room.roomNo === value);
                if (room.roomStatus !== 'vacant')
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
            validator: (rule, value, callback) => {
                if (value[0] === '' || value === '')
                    callback(new Error('时间不能为空')); // 跳过验证  
                else
                    callback(); // 验证通过
            },
            trigger: 'blur'
        },
        {
            validator: (rule, value, callback) => {
                const startDate = new Date(value[0]);
                const endDate = new Date(value[1]);
                if (endDate.getTime() < startDate.getTime())
                    return callback(new Error('结束时间必须大于开始时间'));
                callback(); // 验证通过
            },
            trigger: 'blur'
        }
    ] as Array<FormItemRule>,
});
const customerDialogVisible = ref(false); // 控制弹窗的显示
// 退出对话框时询问
const handleClose = (done: () => void) => {
    showConfirmDialog('信息还未保存，确定退出吗？', '警告')
        .then(() => { done() })
        .catch(() => { })
}
// 关闭对话框重置customerForm
const closeCustomerDialogForm = () => {
    customerDialogVisible.value = false;
    resetCustomerForm();
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
    customerForm.value.resideTimePeriod = ['', '']
}
interface Customer {
    cno: string
    name: string
    idCardNo: string
    mobile: string
    gender: string
    roomNo: string
    checkOutTime: Date
    checkInTime: Date
    image: string
    imageUrl: string
    balance: number
    resideTimePeriod: string[]
    status: string
    user_id?: string
}
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

const userStore = useUserStore();
const isDark = useDark();

const isManager = computed(() => userStore.role === 'manager');
const isCustomer = computed(() => userStore.role === 'customer');

const roomConfigSubmitting = ref(false); // 提交房间配置的状态
const RoomFormSubmitting = ref(false);
const selectedConfig = ref<number | null>(null);
const isAddRoomConfig = ref(false); // 是否正在添加新配置
const isDeleteRoomConfig = ref(false); // 是否正在删除配置
const newConfigName = ref(''); // 新配置的名称
// 响应式数据
const roomData = ref<Room[]>([]);
// 计算属性：是否有房间数据
const hasRooms = computed(() => roomData.value.length > 0);
const size = ref<ComponentSize>('small');
const loading = ref(true);
const currentFloor = ref<Floor>({ title: '一楼', name: '1' }); // 当前楼层
const roomDialogTitle = computed(() => {
    if (roomFormStatus.value === 'isAdding') {
        return '添加房间';
    } else if (roomFormStatus.value === 'isEditing') {
        return `编辑房间：${roomForm.value.roomNo}`;
    } else if (roomFormStatus.value === 'isReserving') {
        return `预订房间：${roomForm.value.roomNo}`;
    } else {
        return '房间详情';
    }
});
const roomDialogVisible = ref(false); // 控制房间表单弹窗的显示
const roomFormStatus = ref(''); // 控制房间表单的状态（添加、编辑、预订、查看）
const allRoomConfigs = ref<{ id: number; name: string; description: string }[]>([]); // 所有 房间配置项
// 类型定义
interface Room {
    roomNo: string;
    roomAmount: number;
    durationType: string;
    roomType: string;
    roomStatus: string;
    imageUrl?: string;
    roomConfig?: string[];
}
interface Floor {
    title: string;
    name: string;
}
// 初始化房间表单
const roomForm = ref<Room>({
    roomNo: '',
    roomAmount: 0,
    durationType: '',
    roomType: '',
    roomStatus: '',
    imageUrl: '',
    roomConfig: [], // 存储配置项的 ID 数组
});
// 房间状态选项
const roomStatusOptions = {
    vacant: { label: '空闲', type: 'success' },
    occupied: { label: '已入住', type: 'primary' },
    maintenance: { label: '维护中', type: 'warning' },
    reserved: { label: '已预订', type: 'info' },
    cleaning: { label: '清洁中', type: 'warning' },
    locked: { label: '锁定', type: 'danger' },
    unavailable: { label: '不可用', type: 'info' },
};
// 表单验证规则
const roomFormRules = {
    roomNo: [{ required: true, message: '请输入房间号', trigger: 'blur' }],
    roomStatus: [{ required: true, message: '请选择房间状态', trigger: 'blur' }],
    roomType: [{ required: true, message: '请选择房间类型', trigger: 'blur' }],
    roomAmount: [{ required: true, message: '请输入房间金额', trigger: 'blur' }],
    durationType: [{ required: true, message: '请选择时间单位', trigger: 'blur' }],
};
// 楼层配置
const floors: Floor[] = [
    { title: '一楼', name: '1' },
    { title: '二楼', name: '2' },
    { title: '三楼', name: '3' },
    { title: '四楼', name: '4' },
    { title: '五楼', name: '5' },
    { title: '六楼', name: '6' },
    { title: '七楼', name: '7' },
    { title: '八楼', name: '8' },
    { title: '九楼', name: '9' },
    { title: '十楼', name: '10' },
];
// 打开添加房间弹窗
const openAddRoomDialog = () => {
    resetRoomForm(); // 重置表单
    roomForm.value.roomAmount = 100;
    roomForm.value.roomStatus = 'vacant'; // 设置默认状态为 "空闲"
    roomFormStatus.value = 'isAdding'; // 设置为添加状态
    roomDialogVisible.value = true; // 打开弹窗
};
// 添加房间
const addRoom = async () => {
    if (roomData.value.some(room => room.roomNo === roomForm.value.roomNo)) {
        ElMessage.error('房间号已存在，请使用其他房间号');
        return;
    }
    try {
        RoomFormSubmitting.value = true; // 提交中状态
        // 检查表单必填项
        if (!roomForm.value.roomNo || !roomForm.value.roomType || !roomForm.value.roomAmount) {
            ElMessage.error('请填写完整的房间信息');
            return;
        }

        // 构造请求数据
        const payload = {
            roomNo: roomForm.value.roomNo,
            roomType: roomForm.value.roomType,
            roomAmount: roomForm.value.roomAmount,
            durationType: roomForm.value.durationType || null, // 可选字段
            roomConfig: roomForm.value.roomConfig.map(configName => {
                const config = allRoomConfigs.value.find(c => c.name === configName);
                return config ? config.id : null;
            }).filter(id => id !== null), // 转换为配置项的 ID 数组
        };

        // 调用后端 API
        const response = await apiClient.post('room/add/', payload);

        if (response.data.code === 1) {
            ElMessage.success('房间添加成功');
            getRoom(); // 重新获取房间数据
            roomDialogVisible.value = false; // 关闭弹窗
            resetRoomForm(); // 重置表单
        } else {
            ElMessage.error(response.data.msg || '房间添加失败');
        }
    } catch (error) { }
    finally {
        RoomFormSubmitting.value = false; // 提交完成状态
    }
};
// 添加房间配置项
const addRoomConfig = async () => {
    try {
        roomConfigSubmitting.value = true; // 提交中状态
        if (!newConfigName.value.trim()) {
            ElMessage.error('配置名称不能为空');
            return;
        }
        if (allRoomConfigs.value.some(config => config.name === newConfigName.value.trim())) {
            ElMessage.error('配置名称已存在，请使用其他名称');
            return;
        }
        const payload = {
            name: newConfigName.value.trim(),
            description: '', // 可选字段，暂时为空
        };
        const response = await apiClient.post('room/config/add/', payload);
        if (response.data.code === 1) {
            ElMessage.success('添加房间配置成功');
            newConfigName.value = ''; // 清空输入框
            getRoomConfig(); // 重新获取房间配置  
            roomForm.value.roomConfig = roomForm.value.roomConfig.filter(name => name !== newConfigName.value); // 同步更新房间配置
        }
    } catch (error) { }
    finally {
        roomConfigSubmitting.value = false; // 提交完成状态
    }
};
// 删除房间配置项
const deleteRoomConfig = async () => {
    if (!newConfigName.value.trim()) {
        ElMessage.error('请输入需要删除的配置名称');
        return;
    }
    const configName = newConfigName.value.trim(); // 捕获当前值
    const configId = allRoomConfigs.value.find(config => config.name === configName)?.id;
    if (!configId) {
        ElMessage.error('配置不存在或已被删除');
        return;
    }
    showConfirmDialog('确定要删除该配置吗？', '提示')
        .then(async () => {
            roomConfigSubmitting.value = true; // 提交中状态
            try {
                const response = await apiClient.delete(`room/config/delete/?config_id=${configId}`);
                if (response.data.code === 1) {
                    ElMessage.success('删除房间配置成功');
                    newConfigName.value = ''; // 清空输入框;
                    getRoomConfig(); // 重新获取房间配置
                    roomForm.value.roomConfig = roomForm.value.roomConfig.filter(name => name !== configName); // 同步更新房间配置

                } else { }
            } catch (error) { }
        })
        .catch(() => {
            ElMessage.info('已取消删除');
        })
        .finally(() => {
            roomConfigSubmitting.value = false; // 提交完成状态
        });
};
// 点击取消
const clear = () => {
    newConfigName.value = ''; // 清空输入框
    isAddRoomConfig.value = false; // 隐藏输入框
    isDeleteRoomConfig.value = false; // 隐藏输入框
};
// 添加配置项
const addFormRoomConfig = (configId: number) => {
    const configName = allRoomConfigs.value.find((config) => config.id === configId)?.name;
    if (configName && !roomForm.value.roomConfig.includes(configName)) {
        roomForm.value.roomConfig.push(configName);
    }
    selectedConfig.value = null; // 清空选择框
};
// 更新房间信息
const updateRoom = async () => {
    try {
        RoomFormSubmitting.value = true; // 提交中状态
        const payload = {
            room_no: roomForm.value.roomNo,
            room_amount: roomForm.value.roomAmount,
            room_type: roomForm.value.roomType,
            duration_type: roomForm.value.durationType,
            room_config: roomForm.value.roomConfig, // 配置项 ID 数组
            room_status: roomForm.value.roomStatus,
        };
        const response = await apiClient.post("room/update/", payload);
        if (response.data.code === 1) {
            ElMessage.success('房间信息更新成功');
            getRoom();
            roomDialogVisible.value = false; // 关闭弹窗
        }
    } catch (error) { }
    finally {
        RoomFormSubmitting.value = false; // 提交完成状态
    }
};
// 打开编辑房间表单弹窗
const openRoomDialog = (room: Room) => {
    if (isCustomer.value) roomFormStatus.value = 'isReserving'; // 设置为预订状态
    else if (isManager.value) roomFormStatus.value = 'isEditing'; // 设置为编辑状态
    else roomFormStatus.value = 'isViewing'; // 设置为查看状态
    roomForm.value = {
        roomNo: room.roomNo || "",
        roomAmount: room.roomAmount || 0,
        durationType: room.durationType || "",
        roomType: room.roomType || "",
        roomStatus: room.roomStatus || "vacant",
        imageUrl: room.imageUrl || "",
        roomConfig: room.roomConfig || [], // 确保 roomConfig 是一个数组
    };
    roomDialogVisible.value = true;
};
// 提交房间表单
const submitRoomForm = () => {
    if (roomFormStatus.value === 'isAdding') {
        addRoom(); // 添加房间
    } else if (roomFormStatus.value === 'isEditing') {
        updateRoom(); // 更新房间信息
    } else if (roomFormStatus.value === 'isReserving') {
        if (roomForm.value.roomStatus !== 'vacant') {
            ElMessage.error('该房间不允许预订');
            return;
        }
        customerForm.value.roomNo = roomForm.value.roomNo; // 设置房间号
        reservedRoom(); // 预订房间
    }
};
// 重置房间表单
const resetRoomForm = () => {
    roomForm.value = {
        roomNo: '',
        roomAmount: 0,
        durationType: '',
        roomType: '',
        roomStatus: '',
        imageUrl: '',
        roomConfig: [],
    };
};
// 切换楼层
const switchFloor = (floor: Floor) => {
    currentFloor.value = floor;
};
// 获取指定楼层的房间
const getFloorRooms = (floor: string): Room[] => {
    if (!floor) return []; // 如果 floor 为空，返回空数组
    return roomData.value.filter((room) => room.roomNo && room.roomNo.startsWith(floor));
};
// 获取房间状态
const getRoomStatus = (room: Room) => {
    const statusMap: Record<string, { type: 'success' | 'danger' | 'warning' | 'info' | 'primary'; status: string }> = {
        vacant: { type: 'success', status: '空闲' },
        occupied: { type: 'primary', status: '已入住' },
        maintenance: { type: 'warning', status: '维护中' },
        reserved: { type: 'info', status: '已预订' },
        cleaning: { type: 'warning', status: '清洁中' },
        locked: { type: 'danger', status: '锁定' },
        unavailable: { type: 'info', status: '不可用' },
    };
    return statusMap[room.roomStatus] || { type: 'primary', status: '未知' };
};
// 图片预览事件
const handlePreview = (file: any) => {
    console.log('预览图片:', file);
};
// 图片移除事件
const handleRemove = (file: any) => {
    console.log('移除图片:', file);
};
// 获取房间数据
const getRoom = async () => {
    try {
        loading.value = true;
        const res = await apiClient.get("room/");
        if (res.data.code === 1) {
            // 解析后端返回的数据
            roomData.value = res.data.data.map((room: any) => ({
                roomNo: room.room_no,
                roomStatus: room.room_status,
                roomType: room.room_type,
                roomAmount: room.room_amount,
                durationType: room.duration_type,
                roomConfig: room.room_config || [], // 确保 roomConfig 存在
            }));
        }
    } finally {
        loading.value = false;
    }
};
// 获取房间配置数据
const getRoomConfig = async () => {
    try {
        // 调用后端 API 获取房间配置
        const response = await apiClient.get("room/config/");
        if (response.data.code === 1) {
            // 更新 allRoomConfigs 数据
            allRoomConfigs.value = response.data.data.map((config: any) => ({
                id: config.id,
                name: config.name,
                description: config.description,
            }));
        }
    } catch (error) { }
};
// 生命周期
onMounted(() => {
    getRoom()
    getRoomConfig()
})
</script>