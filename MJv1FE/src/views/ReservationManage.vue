<template>
    <!-- 面包屑导航 -->
    <el-breadcrumb :separator-icon="ArrowRight" class="no-select mb-4">
        <el-breadcrumb-item to="/Home">首页</el-breadcrumb-item>
        <el-breadcrumb-item>租住记录</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 历史记录表格 -->
    <base-table :table-data="reservations" :columns="columns" :size="'small'" :row-class-name="rowClassName"
        :default-sort="{ prop: 'check_in_time', order: 'descending' }" :max-height="400">

        <template #resideTimePeriod="{ scope }">
            {{ formatResideTime(scope.row.resideTimePeriod[0], scope.row.resideTimePeriod[1]) }}
        </template>
        <!-- 自定义操作列 -->
        <template #actions="{ scope }">
                <el-button type="success" size="small" @click="viewDetails(scope.row)">查看详情</el-button>
                <el-button type="danger" size="small" v-if="scope.row.status === '已预订'"
                    @click="cancelReservation(scope.row)">
                    取消预订
                </el-button>
        </template>
    </base-table>

    <!-- 分页 -->
    <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total"
        :page-sizes="[5, 10, 20, 50]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange"
        @current-change="handleCurrentChange" style="margin-top: 20px; text-align: right;" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import apiClient from '@/services/apiClient'; // 引入封装的 API 客户端
import { ArrowRight } from '@element-plus/icons-vue';
import { useUserStore } from '@/store/userStore';
import BaseTable from '@/components/BaseTable.vue'; // 引入 BaseTable 组件

import { formatResideTime, processResideTimePeriod } from '@/utils/dateUtils'; // 引入时间格式化函数
import showConfirmDialog from '@/utils/showConfirmDialog';

const reservations = ref([]); // 租住记录数据
const total = ref(0); // 总记录数
const currentPage = ref(1); // 当前页码
const pageSize = ref(10); // 每页记录数
const loading = ref(false); // 加载状态

const userStore = useUserStore(); // 获取用户信息

// 表格列配置
const columns = [
    { prop: 'cno', label: '订单号', minWidth: 100, align: 'center' },
    { prop: 'name', label: '姓名', minWidth: 100, align: 'center' },
    { prop: 'room_no', label: '房间号', minWidth: 80, align: 'center' },
    { prop: 'resideTimePeriod', label: '住宿时间', minWidth: 260, showOverflowTooltip: true },
    { prop: 'status', label: '状态', minWidth: 100, align: 'center' },
];

// 取消预订
const cancelReservation = async (row: { cno: string; room_no: string }) => {
    try {
        // 显示确认对话框
        await showConfirmDialog(`确定要取消订单号为 ${row.cno} 的预订吗？，需要支付取消费用`);

        // 调用后端 API
        const { data } = await apiClient.post('/customer/cancel_reserve/', {
            cno: row.cno,
            roomNo: row.room_no,
        });

        if (data.code === 1) {
            ElMessage.success('预订已成功取消');
            fetchReservationHistory(); // 重新加载数据
        }
    }
    catch (error) { }
};

// 获取租住记录数据
const fetchReservationHistory = async () => {
    loading.value = true;
    try {
        const { data } = await apiClient.get(`/reservations/${userStore.userInfo.id}/`);
        if (data.code === 1) {
            reservations.value = data.data.map((item: { resideTimePeriod: any; }) => ({
                ...item,
                resideTimePeriod: processResideTimePeriod(item),
            }));
            total.value = data.data.length;
        } else {
            ElMessage.error(data.msg || '获取租住记录失败');
        }
    } catch (error) {
        ElMessage.error('网络错误，请稍后重试');
    } finally {
        loading.value = false;
    }
};

// 分页处理
const handleSizeChange = (size) => {
    pageSize.value = size;
    fetchReservationHistory();
};

const handleCurrentChange = (page) => {
    currentPage.value = page;
    fetchReservationHistory();
};

// 查看详情
const viewDetails = (row) => {
    ElMessage.info(`查看订单详情：${row.cno}`);
};

// 自定义行样式
const rowClassName = (row) => {
    return row.status === '已退宿' ? 'row-inactive' : '';
};

// 页面加载时获取数据
onMounted(() => {
    fetchReservationHistory();
});
</script>

<style scoped>
.row-inactive {
    background-color: #f5f5f5 !important;
    color: #999 !important;
}
</style>