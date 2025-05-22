<template>
    <el-dialog :model-value="visible" @update:model-value="(val: any) => emit('update:visible', val)" :title="title"
        style="width: 50%" :before-close="beforeClose" draggable @closed="closed" @open="resetForm"
        top="150px" :loading="loading">
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
                        <el-date-picker type="datetimerange" v-model="customerForm.resideTimePeriod" style="width: 100%"
                            :size="size" unlink-panels range-separator="-" format="YYYY-MM-DD HH:mm:ss"
                            start-placeholder="开始" end-placeholder="结束"
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
                <el-button type="primary" v-show="status !== 'VIEW'" @click="onSubmit" :loading="loading">{{
                    submitRemand }}</el-button>
                <el-button type="info" @click="close" v-show="status !== 'VIEW'">取消</el-button>
                <el-button type="primary" v-show="status === 'VIEW'" @click="close">确定</el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { timeDifference } from '@/utils/dateUtils';

enum CustomerDialogStatus {
    NONE = 'none',           // 无状态
    EDIT = 'edit',           // 修改状态
    VIEW = 'view',           // 查看状态
    ADD = 'add',             // 添加状态
    RENEWAL = 'renewal',      // 续租状态
    CHECKINFORSERVED = 'checkInForServed', // 预订顾客办理入住
}

import { Customer } from '@/types/Customer';

const props = defineProps({
    visible: Boolean,
    title: String,
    rules: Object,
    status: String,
    loading: Boolean,
    submitRemand: String,
    customerDialogStatus: {
        type: String,
        default: CustomerDialogStatus.NONE
    },
    size: {
        type: String,
        default: 'default'
    },
    customerForm: {
        type: Object as () => Customer,
        default: () => ({
            cno: '',
            name: '',
            idCardNo: '',
            mobile: '',
            gender: '',
            roomNo: '',
            checkOutTime: null,
            checkInTime: null,
            image: '',
            imageUrl: '',
            balance: 0,
            resideTimePeriod: [],
            status: ''
        })
    },
    beforeClose: {
        type: Function,
        default: () => {}
    }
});
const emit = defineEmits(['closeCustomerDialogForm', 'resetForm', 'update:visible', 'submit', 'before-close', 'closed', 'uploadPicturePost', 'beforeAvatarUpload', 'uploadPicturePost', 'roomMessage']);

const ruleFormRef = ref();

const close = () => emit('closeCustomerDialogForm');
const onSubmit = () => emit('submit', ruleFormRef.value);
// const handleClose = (done: () => void) => emit('before-close', done);
const beforeAvatarUpload = (file: File) => emit('beforeAvatarUpload', file);
const uploadPicturePost = (file: File) => emit('uploadPicturePost', file);
const resetForm = () => emit('resetForm', ruleFormRef.value);
const roomMessage = (roomNo: string) => emit('roomMessage', roomNo);
const closed = () => emit('closed');
</script>