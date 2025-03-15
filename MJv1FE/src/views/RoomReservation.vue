<template>
    <el-breadcrumb :separator-icon="ArrowRight" class="no-select">
        <el-breadcrumb-item to="/Home">首页</el-breadcrumb-item>
        <el-breadcrumb-item>预订房间</el-breadcrumb-item>
    </el-breadcrumb>
    <el-collapse accordion>
        <el-collapse-item title="一楼" name="1">
            <el-button v-for="(item, index) in roomData" plain :key="index" :icon="Search" type="primary" :size="size">
                {{ item.roomNo }}
            </el-button>
        </el-collapse-item>
        <el-collapse-item title="二楼" name="2"><el-button v-for="(item, index) in roomData" plain :key="index"
                :icon="Search" type="primary" :size="size">
                {{ item.roomNo }}
            </el-button>
        </el-collapse-item>
        <el-collapse-item title="三楼" name="3"><el-button v-for="(item, index) in roomData" plain :key="index"
                :icon="Search" type="primary" :size="size">
                {{ item.roomNo }}
            </el-button>
        </el-collapse-item>
        <el-collapse-item title="四楼" name="4"><el-button v-for="(item, index) in roomData" plain :key="index"
                :icon="Search" type="primary" :size="size">
                {{ item.roomNo }}
            </el-button>
        </el-collapse-item>
    </el-collapse>
</template>

<script lang="ts" setup>
import { ArrowRight, Search } from '@element-plus/icons-vue'
import { ComponentSize } from 'element-plus'
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '@/services/apiClient';


const roomData = ref<Room[]>([])                              // 储存请求信息

const size = ref<ComponentSize>('small')                           // 组件大小
// 设置默认的 baseURL  


interface Room {
    roomNo: string
    roomAmount: number
    durationType: string
    roomType: string
}

onMounted(() => {
    getRoom();
})
const getRoom = () => {
    apiClient
        .get("room/")
        .then(function (res) {
            // 请求成功后执行的函数
            if (res.data.code === 1) {
                roomData.value = res.data.data
                // console.log(roomData.value)
                // ElMessage({
                //     message: '加载成功',
                //     type: 'success',
                //     plain: true,
                //     showClose: true,
                // })
            } else {
                ElMessage({
                    message: res.data.msg,
                    type: 'error',
                    showClose: true,
                    plain: true,
                })
            }
        })
        .catch(function (err) {
            if (err.status == 401)
                ElMessage.warning("请先登录")
            else {
                console.error(err)
                ElMessage.error("获取后端结果错误")
            }
        })
}
</script>