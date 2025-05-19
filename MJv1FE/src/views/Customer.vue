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
                <!-- <el-col :span="2" class="upload-container">
                <el-upload>
                    <el-button type="primary" plain>导入excel</el-button>
                </el-upload>
            </el-col>
            <el-col :span="2" class="export-container">
                <el-button type="primary" plain>导出excel</el-button>
            </el-col> -->
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
        <el-dialog v-model="customerDialogVisible" :title="customerDialogTitle" style="width: 50%"
            :before-close="handleClose" draggable @closed="closeCustomerDialogForm" @open="resetForm(ruleFormRef)"
            top="150px">
            <el-form :inline="true" label-width="110px" label-position="right" :model="customerForm" :rules="rules"
                ref="ruleFormRef">
                <el-row style="display: flex; align-items: center;">
                    <el-col :span="12" style="padding-right: 5px;">
                        <el-form-item label="编号" prop="cno" v-show="customerDialogStatus !== CustomerDialogStatus.ADD">
                            <el-input style="width: 100%;" v-model="customerForm.cno" :size="size" disabled
                                v-show="customerDialogStatus !== CustomerDialogStatus.ADD"></el-input>
                        </el-form-item>
                        <el-form-item label="姓名" prop="name">
                            <el-input style="width: 100%;" v-model="customerForm.name" :size="size"
                                :disabled="customerDialogStatus === CustomerDialogStatus.VIEW || customerDialogStatus === CustomerDialogStatus.RENEWAL"></el-input>
                        </el-form-item>
                        <el-form-item label="身份号" prop="idCardNo">
                            <el-input style="width: 100%;" v-model="customerForm.idCardNo" :size="size"
                                :disabled="customerDialogStatus === CustomerDialogStatus.VIEW || customerDialogStatus === CustomerDialogStatus.RENEWAL"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12" style="padding-right: 5px;"> <!-- 证件照部分 -->
                        <el-form-item label="证件照">
                            <el-upload class="avatar-uploader" :action="customerForm.imageUrl" :show-file-list="false"
                                :before-upload="beforeAvatarUpload" style="text-align: center;" :size="size"
                                :http-request="uploadPicturePost"
                                :disabled="customerDialogStatus === CustomerDialogStatus.VIEW || customerDialogStatus === CustomerDialogStatus.RENEWAL">
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
                            <el-input v-model="customerForm.mobile" :size="size"
                                :disabled="customerDialogStatus === CustomerDialogStatus.VIEW || customerDialogStatus === CustomerDialogStatus.RENEWAL"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="余额" prop="balance">
                            <el-input v-model="customerForm.balance" :size="size"
                                :disabled="customerDialogStatus === CustomerDialogStatus.VIEW"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row style="align-items: center;" v-show="customerDialogStatus !== CustomerDialogStatus.ADD">
                    <el-col :span="12" style="padding-right: 5px;">
                        <el-form-item label="登记时间" prop="checkInTime">
                            <el-date-picker v-model="customerForm.checkInTime" type="datetime" placeholder="未登记"
                                :size="size" style="width: 100%" disabled />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12" style="padding-left: 5px;">
                        <el-form-item label="退宿时间" prop="checkOutTime" disabled>
                            <el-date-picker v-model="customerForm.checkOutTime" type="datetime" placeholder="未退宿"
                                :size="size" style="width: 100%" disabled />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="10" style="padding-left: 5px;">
                        <el-form-item label="房间号" prop="roomNo">
                            <el-input v-model="customerForm.roomNo" :size="size"
                                :disabled="customerDialogStatus === CustomerDialogStatus.VIEW || customerDialogStatus === CustomerDialogStatus.RENEWAL"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6" style="padding-left: 5px;padding-top: 5px;">
                        <el-text style="width: 100%" :size="size">{{ roomMessage(customerForm.roomNo)
                            }}</el-text>
                    </el-col>
                    <el-col :span="8" style="padding-left: 5px;">
                        <el-form-item label="性别" prop="gender" label-width="40px">
                            <el-radio-group v-model="customerForm.gender" :size="size"
                                :disabled="customerDialogStatus === CustomerDialogStatus.VIEW || customerDialogStatus === CustomerDialogStatus.RENEWAL"
                                style="width: 185px;" fill="#909399">
                                <el-radio-button value="男">男</el-radio-button>
                                <el-radio-button value="女">女</el-radio-button>
                            </el-radio-group>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row>
                    <el-col :span="18" style="padding-left: 5px;">
                        <el-form-item label="入住时间" prop="resideTimePeriod">
                            <el-date-picker type="datetimerange" v-model="customerForm.resideTimePeriod"
                                style="width: 100%" :size="size" unlink-panels range-separator="-"
                                format="YYYY-MM-DD HH:mm:ss" start-placeholder="开始" end-placeholder="结束"
                                :disabled="customerDialogStatus === CustomerDialogStatus.VIEW || customerDialogStatus === CustomerDialogStatus.EDIT"
                                placement="top-start" />
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
                    <el-button type="primary" v-show="customerDialogStatus !== CustomerDialogStatus.VIEW"
                        @click="submitForm(ruleFormRef)" :loading="isSubmitting">{{
                            submitRemand }}</el-button>
                    <el-button type="info" @click="customerDialogVisible = false"
                        v-show="customerDialogStatus !== CustomerDialogStatus.VIEW">取消</el-button>
                    <el-button type="primary" v-show="customerDialogStatus === CustomerDialogStatus.VIEW"
                        @click="customerDialogVisible = false">确定</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import BaseTable from '@/components/BaseTable.vue';

const columns = [
    { prop: 'name', label: '姓名', minWidth: 50, showOverflowTooltip: true },
    { prop: 'roomNo', label: '房间号', minWidth: 80, sortable: true },
    { prop: 'balance', label: '余额', minWidth: 70, showOverflowTooltip: true },
    { prop: 'status', label: '状态', minWidth: 70, showOverflowTooltip: true },
    { prop: 'resideTimePeriod', label: '住宿时间', minWidth: 260, showOverflowTooltip: true },
    { prop: 'idCardNo', label: '身份证', minWidth: 150, showOverflowTooltip: true },
    { prop: 'mobile', label: '电话号码', minWidth: 100, showOverflowTooltip: true },
];

import showConfirmDialog from '@/utils/showConfirmDialog';

const isSubmitting = ref(false); // 控制按钮的加载状态
const roomMessage = (roomNo: string) => {
    const roomInfo = roomData.value.find(room => room.roomNo === roomNo) || null;
    if (roomNo === '' || roomInfo === null)
        return '';
    else {
        const roomAmount = roomInfo ? roomInfo.roomAmount || '未知' : '未找到房间';
        return `单价${roomAmount})`;
    }
}

const deposit = 100;//押金

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
// 退租
const checkOut = (row: { resideTimePeriod: (string | number | Date)[]; roomNo: string; name: string; balance: number; cno: any; }) => {
    const startDate = new Date(row.resideTimePeriod[0]);
    const endDate = new Date(row.resideTimePeriod[1]);

    let timeDifference: number = endDate.getTime() - startDate.getTime();
    const info = roomData.value.find(room => room.roomNo === row.roomNo);
    let minimumAmount: number
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
const renewal = (row: { resideTimePeriod: string[]; cno: any }) => {
    oldResideTimePeriod.value = row.resideTimePeriod;
    initializeCustomerForm(row, { resideTimePeriod: ['', ''] }); // 清空居住时间
    customerDialogStatus.value = CustomerDialogStatus.RENEWAL;
    customerDialogVisible.value = true;
};

// 预订顾客办理入住
const checkInForServed = (row: { resideTimePeriod: string[]; cno: any }) => {
    initializeCustomerForm(row, {
        checkInTime: new Date(),
        status: '已入住',
    }); // 设置入住时间和状态
    customerDialogStatus.value = CustomerDialogStatus.CHECKINFORSERVED;
    customerDialogVisible.value = true;
};
const initializeCustomerForm = (row: any, overrides: Partial<Customer> = {}) => {
    // 深拷贝 row 数据到 customerForm
    customerForm.value = { ...JSON.parse(JSON.stringify(row)) };

    // 获取图片并拼接 URL
    customerForm.value.image = getImage(row.cno);
    customerForm.value.imageUrl = `${apiClient.defaults.baseURL}media/${customerForm.value.image}`;

    // 应用 overrides 参数覆盖指定字段
    Object.assign(customerForm.value, overrides);
};
import { computed, onMounted, ref } from 'vue'
import { Search, Delete, Edit, Refresh, More, FolderOpened, Plus, ArrowRight } from '@element-plus/icons-vue'
import { dayjs, ElMessage, FormItemRule, ComponentSize, FormInstance, UploadProps } from 'element-plus'
import apiClient from '@/services/apiClient';
import { AxiosResponse } from 'axios';

// 定义对话框状态枚举
enum CustomerDialogStatus {
    NONE = 'none',           // 无状态
    EDIT = 'edit',           // 修改状态
    VIEW = 'view',           // 查看状态
    ADD = 'add',             // 添加状态
    RENEWAL = 'renewal',      // 续租状态
    CHECKINFORSERVED = 'checkInForServed', // 预订顾客办理入住
}

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
            validator: (rule, value, callback) => {
                const startDate = new Date(customerForm.value.resideTimePeriod[0]);
                const endDate = new Date(customerForm.value.resideTimePeriod[1]);

                let timeDifference: number = endDate.getTime() - startDate.getTime();
                const info = roomData.value.find(room => room.roomNo === customerForm.value.roomNo);

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
}
interface Room {
    roomNo: string;
    roomAmount: number;
    durationType: string;
    roomType: string;
    roomStatus: string;
    imageUrl?: string;
    roomConfig?: string[];
    status?: string;
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
const tableRowClassName = ({ row }: { row: Customer }) => {
    const now = dayjs();
    const resideTimePeriod = dayjs(row.resideTimePeriod[1], undefined, true)
    if (row.status == '已退宿') return ''
    else if (resideTimePeriod.isBefore(now)) return 'danger-row'; // 过期
    else if (resideTimePeriod.isAfter(now.add(1, 'day'))) return 'success-row'; // 正常
    else return 'warning-row'; // 即将到期
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
import { formatResideTime, processResideTimePeriod } from '@/utils/dateUtils'; // 引入工具函数

// ————————————————————————————————————————————————————————————————————————————————————————————操作—————————————————————————————————————————————————————————————————————————————————— //
const customerDialogVisible = ref(false) // 显示dialog
// 获取所有房客信息
const getCustomer = () => {
    inputStr.value = '';
    apiClient
        .get("customer/")
        .then((res) => {
            // 请求成功后执行的函数
            if (res.data.code === 1) {
                flushedDate(res);
            }
        })
        .finally(() => {
        })
}
// 根据返回值重新加载页面（customerDate和total.value赋值）
const flushedDate = (res: AxiosResponse<any, any>) => {
    customerDate.value = res.data.data.map((item: any) => ({
        ...item,
        roomNo: item.room_id,
        resideTimePeriod: processResideTimePeriod(item), // 自定义处理函数
    }));
    total.value = res.data.data.length;
    getPageCustomer();
}
const getRoom = async () => {
    try {
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
    }
};
// 显示查看明细对话框
const viewCustomer = (row: { cno: any }) => {
    initializeCustomerForm(row); // 不需要额外覆盖字段
    customerDialogStatus.value = CustomerDialogStatus.VIEW;
    customerDialogVisible.value = true;
};
// 显示修改信息对话框
const updateCustomer = (row: { cno: any }) => {
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
    customerForm.value.resideTimePeriod = ['', '']
}
// 关闭对话框重置customerForm
const closeCustomerDialogForm = () => {
    customerDialogVisible.value = false;
    resetCustomerForm();
    customerDialogStatus.value = CustomerDialogStatus.NONE;
}
// 重置验证信息
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
    if (!formEl) return
    formEl.clearValidate()
}
const ruleFormRef = ref<FormInstance>()
// 校验
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    isSubmitting.value = true; // 开始加载
    try {
        await formEl.validate((valid, fields) => {
            if (valid) {
                if (customerDialogStatus.value === CustomerDialogStatus.ADD) submitAddCustomer();
                else submitUpdateCustomer();
            }
        });
    } finally {
        isSubmitting.value = false; // 提交完成后停止加载
    }
};
// 查询
const queryCustomer = () => {
    apiClient
        .post('customer/query/', { inputstr: inputStr.value })
        .then((res) => {
            if (res.data.code === 1) {
                flushedDate(res);
                ElMessage.success('查询成功')
            }
        })
}
const submitUpdateCustomer = async () => {
    return apiClient
        .post("customer/update/", customerForm.value)
        .then((res) => {
            if (res.data.code === 1) {
                flushedDate(res);
                ElMessage.success('修改成功');
                closeCustomerDialogForm();
            } else return Promise.reject(new Error(res.data.msg));
        })
        .catch((err) => {
            return Promise.reject(err);
        });
};
// 提交添加
const submitAddCustomer = () => {
    const now = new Date();
    customerForm.value.checkInTime = now;
    customerForm.value.status = '已入住';
    apiClient
        .post("customer/add/", customerForm.value)
        .then((res) => {
            if (res.data.code === 1) {
                flushedDate(res);

                ElMessage.success('办理入住成功')
                closeCustomerDialogForm()
            }
        })
}
// 删除
const deleteCustomer = (row: { name: string; cno: any; }) => {
    showConfirmDialog('是否永久删除姓名为' + row.name + '的顾客信息?', '警告')

        .then(() => {
            apiClient
                .post("customer/delete/", row.cno)
                .then((res) => {
                    // 请求成功后执行的函数
                    if (res.data.code === 1) {
                        flushedDate(res);
                        ElMessage.success('删除成功')
                        closeCustomerDialogForm()
                    }
                })
        })
        .catch()
}
// 批量删除
const selectCustomers = ref([])
const handleSelectionChange = (data: any[]) => {
    selectCustomers.value = data
}
const deleteCustomers = (row: any) => {
    showConfirmDialog('是否批量删除' + selectCustomers.value.length + '个顾客的信息?', '警告')
        .then(() => {
            apiClient
                .post("customers/delete/", { customers: selectCustomers.value })
                .then((res) => {
                    // 请求成功后执行的函数
                    if (res.data.code === 1) {
                        flushedDate(res);
                        ElMessage.success('批量删除成功')
                        closeCustomerDialogForm()
                    }
                })
        })
        .catch()
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
// 根据id获取image
const getImage = (cno: string) => {
    for (let oneCustomer of customerDate.value) {
        if (oneCustomer.cno === cno) {
            return oneCustomer.image;
        }
    }
}
</script>
