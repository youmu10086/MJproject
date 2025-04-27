<template>
    <el-dialog v-model="messageCardDisplay" class="custom-dialog" :show-close="false" align-center>
        <el-scrollbar max-height="400px" wrap-style="padding-right: 10px;">
            <span>
                <h3>Tips</h3>
                🌟 <strong>美家公寓管理平台</strong> 是一款专为公寓管理打造的智能化解决方案，集房间管理 🏠、用户管理 👥、在线服务 💬、预订管理 📅、反馈处理 📢 等功能于一体。
                <br />
                🚀 平台通过简洁直观的界面设计和高效的操作流程，帮助公寓管理者轻松掌控日常运营，提高管理效率 📈，优化客户体验 😊，为公寓的数字化转型提供强有力的支持。
                <br /><br />
                ⚠️ <strong>本网页目前处于开发阶段</strong>，现已实现以下功能：
                <ul>
                    <li>🏨 客房展示</li>
                    <li>📋 顾客预订、入住、续租、退房</li>
                    <li>🛠️ 后台入住管理</li>
                    <li>👤 用户管理</li>
                </ul>
                🔧 后续将逐步完善以下功能，敬请期待：
                <ul>
                    <li>💬 在线客服</li>
                    <li>⭐ 评价反馈</li>
                    <li>👥 用户管理</li>
                </ul>
                <br />
                🔑 <strong>测试账号信息：</strong>
                <ul>
                    <li>👤 顾客账号：<code>customer</code> 密码：<code>666666</code></li>
                    <li>👤 管理员账号：<code>admin</code> 密码：<code>666666</code></li>
                    <li>👤 业务员账号：<code>manager</code> 密码：<code>666666</code></li>
                </ul>
            </span>
        </el-scrollbar>

        <!-- 按钮固定在右下角 -->
        <el-affix class="dialog-button-affix">
            <el-button type="primary" @click="closeDialog">确定</el-button>
        </el-affix>
    </el-dialog>
</template>

<script lang="ts" setup>
import { useMessageCardStore } from '@/store/messageCardStore';
import { computed } from 'vue';

// 引入 Pinia Store
const messageCardStore = useMessageCardStore();

// 计算属性，获取对话框是否显示状态
const messageCardDisplay = computed(() => !messageCardStore.messageCardIsDisplayed);

// 手动关闭对话框
const closeDialog = () => messageCardStore.setMessageCardDisplayed(true);
</script>

<style scoped>
.custom-dialog {
    width: 60%;
    max-height: 80vh;
    position: relative;
}

/* 按钮固定在右下角 */
.dialog-button-affix {
    position: absolute;
    bottom: 20px;
    right: 40px;
}
</style>