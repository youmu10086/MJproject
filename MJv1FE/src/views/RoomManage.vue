<template>
    <el-breadcrumb :separator-icon="ArrowRight" class="no-select mb-4">
        <el-breadcrumb-item to="/Home">首页</el-breadcrumb-item>
        <el-breadcrumb-item>公寓房间管理</el-breadcrumb-item>
    </el-breadcrumb>
    <div class="container" :class="{ dark: isDark }">
        <div class="room-management">
            <el-skeleton :rows="5" animated v-if="loading" />
            <el-empty v-else-if="!hasRooms" description="暂无房间数据" />
            <template v-else>
                <el-card shadow="hover" class="floor-card">
                    <template #header>
                        <div class="floor-header">
                            <span class="floor-title">当前楼层：{{ currentFloor.title }}</span>
                            <el-button-group>
                                <el-button v-for="floor in floors" :key="floor.name"
                                    :type="floor.name === currentFloor.name ? 'primary' : 'default'"
                                    @click="switchFloor(floor)">
                                    {{ floor.title }}
                                </el-button>
                            </el-button-group>
                            <el-button-group class="right-aligned">
                                <el-button @click="openAddRoomDialog">添加房间</el-button>
                                <el-button>添加楼层</el-button>
                            </el-button-group>
                        </div>
                    </template>

                    <el-row v-if="getFloorRooms(currentFloor.name).length" :gutter="12">
                        <el-col v-for="room in getFloorRooms(currentFloor.name)" :key="room.roomNo || Math.random()"
                            :xs="12" :sm="8" :md="6" :lg="4" :xl="8" class="room-col">
                            <el-button class="room-button" :type="getRoomStatus(room).type" :size="size"
                                @click="openEditRoomDialog(room)" :plain="true">
                                <div class="room-info">
                                    <span class="room-number">{{ room.roomNo || '未知房间号' }}</span>
                                    <el-tag v-if="getRoomStatus(room).status" :type="getRoomStatus(room).type"
                                        size="small" class="mt-1">
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
    </div>
    <el-dialog v-model="roomDialogVisible" :title="dialogTitle" width="900px" :close-on-click-modal="false"
        @closed="resetRoomForm">
        <!-- 使用 header 插槽自定义标题 -->
        <template #header>
            <div style="display: flex; align-items: center;">
                <span>{{ isAddRoom ? '添加房间' : dialogTitle }}</span>
                <el-input v-if="isAddRoom" v-model="roomForm.roomNo" placeholder="请输入房间号" size="small"
                    style="margin-left: 10px; width: 100px;" />
            </div>
        </template>
        <el-form :model="roomForm" :rules="roomFormRules" ref="formRef" label-width="120px" label-position="right"
            class="optimized-form">
            <div class="form-section">
                <el-row :gutter="30">
                    <el-col :xs="24" :sm="12" :md="8">
                        <el-form-item label="房间状态" prop="roomStatus">
                            <el-select v-model="roomForm.roomStatus" placeholder="请选择" class="full-width">
                                <el-option v-for="(status, key) in roomStatusOptions" :key="key" :label="status.label"
                                    :value="key" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="12" :md="8">
                        <el-form-item label="房间类型" prop="roomType">
                            <el-input v-model="roomForm.roomType" placeholder="请输入类型" clearable class="full-width" />
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="12" :md="8">
                        <el-form-item label="时间单位" prop="durationType">
                            <el-select v-model="roomForm.durationType" placeholder="请选择时间单位" class="full-width">
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
                                class="amount-input">
                                <template #append>元</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="16">
                        <el-form-item label="房间配置">
                            <div class="config-tag-group">
                                <el-select v-model="roomForm.roomConfig" multiple placeholder="添加配置"
                                    class="add-config-tag" @change="addFormRoomConfig">
                                    <el-option v-for="config in allRoomConfigs" :key="config.id" :label="config.name"
                                        :value="config.name" />
                                    <template #footer>
                                        <el-button v-if="!isAdding && !isDelete" text bg size="small"
                                            @click="isAdding = true">
                                            添加配置
                                        </el-button>
                                        <template v-if="isAdding">
                                            <el-input v-model="newConfigName" class="option-input"
                                                placeholder="输入需要添加的配置名称" size="small" />
                                            <el-button type="primary" size="small" @click="addRoomConfig">
                                                确认
                                            </el-button>
                                            <el-button size="small" @click="clear">取消</el-button>
                                        </template>
                                        <el-button v-if="!isAdding && !isDelete" text bg size="small"
                                            @click="isDelete = true;">
                                            删除配置
                                        </el-button>
                                        <template v-if="isDelete">
                                            <el-input v-model="newConfigName" class="option-input"
                                                placeholder="输入需要删除的配置名称" size="small" />
                                            <el-button type="primary" size="small" @click="deleteRoomConfig">
                                                确认
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
                <el-button type="primary" @click="submitRoomForm" size="small" :loading="submitting">
                    {{ submitting ? '提交中...' : '确认' }}
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { ArrowRight } from '@element-plus/icons-vue';
import { ComponentSize, ElMessageBox } from 'element-plus';
import { onMounted, ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import apiClient from '@/services/apiClient';
import { useDark } from '@vueuse/core';
const isDark = useDark();

const submitting = ref(false);
const selectedConfig = ref<number | null>(null);
const isAdding = ref(false); // 是否正在添加新配置
const isDelete = ref(false); // 是否正在删除配置
const newConfigName = ref(''); // 新配置的名称
// 响应式数据
const roomData = ref<Room[]>([]);
// 计算属性：是否有房间数据
const hasRooms = computed(() => roomData.value.length > 0);
const size = ref<ComponentSize>('small');
const loading = ref(true);
const currentFloor = ref<Floor>({ title: '一楼', name: '1' }); // 当前楼层
const dialogTitle = ref('编辑房间信息');
const roomDialogVisible = ref(false); // 控制房间表单弹窗的显示
const isAddRoom = ref(false); // 控制添加房间弹窗的显示
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
const allRoomConfigs = ref<{ id: number; name: string; description: string }[]>([]);
// 打开添加房间弹窗
const openAddRoomDialog = () => {
    resetRoomForm(); // 重置表单
    roomForm.value.roomAmount = 100; // 清空房间号
    roomForm.value.roomStatus = 'vacant'; // 设置默认状态为 "空闲"
    dialogTitle.value = '添加房间'; // 设置弹窗标题
    isAddRoom.value = true; // 设置添加房间标志
    roomDialogVisible.value = true; // 打开弹窗
};
// 添加房间
const addRoom = async () => {
    if (roomData.value.some(room => room.roomNo === roomForm.value.roomNo)) {
        ElMessage.error('房间号已存在，请使用其他房间号');
        return;
    }
    try {
        // 检查表单必填项
        if (!roomForm.value.roomNo || !roomForm.value.roomType || !roomForm.value.roomAmount) {
            console.log('房间号:', roomForm.value.roomNo);
            console.log('房间类型:', roomForm.value.roomType);
            console.log('房间金额:', roomForm.value.roomAmount);
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
};
// 添加房间配置项
const addRoomConfig = async () => {
    try {
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
    ElMessageBox.confirm('确定要删除该配置吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    })
        .then(async () => {
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
        });
};
// 点击取消
const clear = () => {
    newConfigName.value = ''; // 清空输入框
    isAdding.value = false; // 隐藏输入框
    isDelete.value = false; // 隐藏输入框
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
};
// 打开编辑房间表单弹窗
const openEditRoomDialog = (room: Room) => {
    roomForm.value = {
        roomNo: room.roomNo || "",
        roomAmount: room.roomAmount || 0,
        durationType: room.durationType || "",
        roomType: room.roomType || "",
        roomStatus: room.roomStatus || "vacant",
        imageUrl: room.imageUrl || "",
        roomConfig: room.roomConfig || [], // 确保 roomConfig 是一个数组
    };
    dialogTitle.value = `编辑房间：${room.roomNo}`;
    roomDialogVisible.value = true;
};
// 提交房间表单
const submitRoomForm = () => {
    isAddRoom ? addRoom() : updateRoom();
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
        console.log('房间数据:', roomData.value);
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

<style scoped>
.option-input {
    width: 150px;
    margin-right: 8px;
}

.add-config-tag {
    flex-grow: 1;
    width: 400px;
    display: inline-block;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.config-tag-group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
}

.config-tag {
    margin: 0;
}

.optimized-form {
    padding: 0;
}

:root {
    --card-bg: #CDD0D6;
}

.dark {
    --card-bg: #409eff;
}

.optimized-form .form-section {
    margin-bottom: 10px;
    padding: 10px;
    background: var(--card-bg);
    border-radius: 8px;
}

.dialog-footer {
    text-align: right;
}

.dialog-footer .el-button {
    min-width: 100px;
    margin-left: 15px;
}

.container {
    padding: 20px 0 20px 0;
    max-width: 1400px;
    margin: 0 auto;
}

.floor-card {
    border-radius: 12px;
    transition: transform 0.3s ease;
}

.floor-card:hover {
    transform: translateY(-2px);
}

.floor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.room-col {
    padding: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.room-button {
    height: 60px;
    width: 70%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.room-button:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.room-info {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.room-number {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 4px;
}
</style>