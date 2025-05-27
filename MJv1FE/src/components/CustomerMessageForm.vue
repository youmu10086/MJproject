<template>
    <teleport to='#app'>
        <el-dialog v-model="visible" :title="title" :before-close="beforeClose" draggable @closed="closed"
            @open="resetForm" top="150px" :loading="loading" fullscreen>
            <el-form :inline="true" label-width="110px" label-position="right" :model="customerForm" :rules="rules"
                ref="ruleFormRef">
                <el-row style="display: flex; align-items: center;">
                    <el-col :span="12" style="padding-right: 5px;">
                        <el-form-item label="编号" prop="cno"
                            v-show="customerDialogStatus !== CustomerDialogStatus.ADD && customerDialogStatus !== CustomerDialogStatus.CUSTOMERRSERVED">
                            <el-input style="width: 100%;" v-model="customerForm.cno" :size="size" disabled></el-input>
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
                <el-row style="align-items: center;"
                    v-show="customerDialogStatus !== CustomerDialogStatus.ADD && customerDialogStatus !== CustomerDialogStatus.CUSTOMERRSERVED">
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
                <!-- 其余 el-row ... -->
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" v-show="customerDialogStatus !== CustomerDialogStatus.VIEW"
                        @click="submit" :loading="loading">{{
                            submitRemand }}</el-button>
                    <el-button type="primary" v-show="customerDialogStatus === CustomerDialogStatus.VIEW"
                        @click="close">确定</el-button>
                    <el-button type="info" @click="close"
                        v-show="customerDialogStatus !== CustomerDialogStatus.VIEW">取消</el-button>
                </div>
            </template>
        </el-dialog>
    </teleport>
</template>

<script setup lang="ts">
defineOptions({ name: 'CustomerMessageForm' });
import { ref } from 'vue';
import { timeDifference } from '@/utils/dateUtils';
import { Customer, CustomerDialogStatus } from '@/types/Customer';
import { ComponentSize } from 'element-plus';
const customerForm = defineModel<Customer>('customerForm', {
    // 添加完整的默认值对象
    default: () => ({
        cno: '',
        name: '',
        idCardNo: '',
        mobile: '',
        gender: '男',
        roomNo: '',
        checkOutTime: null,
        checkInTime: null,
        image: '',
        imageUrl: '',
        balance: 0,
        resideTimePeriod: ['', ''],
        status: '',
    }),
    required: true,
});

const visible = defineModel('visible', {
    default: false,
    type: Boolean
});

defineProps({
    // visible: Boolean,
    title: String,
    rules: Object,
    loading: Boolean,
    submitRemand: String,
    customerDialogStatus: {
        type: String as () => CustomerDialogStatus,
        default: CustomerDialogStatus.NONE
    },
    size: {
        type: String as () => ComponentSize,
        default: 'default'
    },
    beforeClose: {
        type: Function,
        default: () => { }
    }
});
const ruleFormRef = ref();

const emit = defineEmits([
    'close',
    'resetForm',
    //   'update:visible',
    'submit',
    'before-close',
    'closed',
    'uploadPicturePost',
    'beforeAvatarUpload',
    'roomMessage'
]);


const close = () => emit('close');
const submit = () => emit('submit', ruleFormRef.value);
const beforeAvatarUpload = (file: File) => emit('beforeAvatarUpload', file);
const uploadPicturePost = (file: File) => emit('uploadPicturePost', file);
const resetForm = () => emit('resetForm', ruleFormRef.value);
const roomMessage = (roomNo: string) => emit('roomMessage', roomNo);
const closed = () => emit('closed');
</script>