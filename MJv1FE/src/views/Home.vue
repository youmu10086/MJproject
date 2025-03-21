<template>

  <el-scrollbar>

    <div class="home-page">
      <header class="header">
        <h1>美佳公寓智能管理平台</h1>
        <p>高效、便捷、智能的公寓管理解决方案</p>
      </header>

      <el-carousel indicator-position="outside" trigger="click" class="carousel">
        <el-carousel-item v-for="item in carouselItems" :key="item.id">
          <h3 class="carousel-item">{{ item.text }}</h3>
        </el-carousel-item>
      </el-carousel>

      <div class="info-section">
        <el-row>
          <el-col :span="6">
            <el-statistic title="每日活跃用户" :value="17" />
          </el-col>
          <el-col :span="6">
            <el-statistic :value="138">
              <template #title>
                <div class="statistic-title">
                  性别比例
                  <el-icon style="margin-left: 4px" :size="12">
                    <Male />
                  </el-icon>
                </div>
              </template>
              <template #suffix>/100</template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="总交易量" :value="outputValue" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="反馈数量" :value="562">
              <template #suffix>
                <el-icon style="vertical-align: -0.125em">
                  <ChatLineRound />
                </el-icon>
              </template>
            </el-statistic>
          </el-col>
        </el-row>
      </div>

      <div class="demo-collapse">
        <el-row>
          <el-col :span="24">

            <el-collapse v-model="activeName" accordion>
              <el-collapse-item title="平台功能" name="1">
                <div>
                  <p>1. 物业管理：提供全面的物业管理工具，简化日常运营。</p>
                  <p>2. 费用管理：实时跟踪和管理公寓费用，自动生成账单。</p>
                  <p>3. 住户服务：为住户提供便捷的服务请求和反馈渠道。</p>
                </div>
              </el-collapse-item>
              <el-collapse-item title="数据分析" name="2">
                <div>
                  <p>通过数据分析，帮助管理者了解住户需求和运营效率。</p>
                  <p>实时监控关键指标，做出数据驱动的决策。</p>
                </div>
              </el-collapse-item>
              <el-collapse-item title="安全监控" name="3">
                <div>
                  <p>提供实时的安全监控服务，确保住户的安全和隐私。</p>
                  <p>支持远程监控和报警功能，及时响应突发事件。</p>
                </div>
              </el-collapse-item>
              <el-collapse-item title="社区互动" name="4">
                <div>
                  <p>促进住户之间的互动，建立和谐的社区氛围。</p>
                  <p>提供公告、活动通知等功能，增强社区参与感。</p>
                </div>
              </el-collapse-item>
            </el-collapse>
          </el-col>
        </el-row>
      </div>
    </div>
  </el-scrollbar>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useTransition } from '@vueuse/core'
import { ChatLineRound, Male } from '@element-plus/icons-vue'

const activeName = ref('1')
const carouselItems = ref([
  { id: 1, text: '智能管理，便捷生活' },
  { id: 2, text: '高效服务，满意体验' },
  { id: 3, text: '全面监控，安全无忧' },
  { id: 4, text: '数据分析，决策支持' },
]);

const source = ref(0)
const outputValue = useTransition(source, {
  duration: 1500,
})
source.value = 172000  
</script>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.home-page {
  font-family: 'Arial', sans-serif;
  padding: 20px;
  background-color: #f5f7fa;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.header h1 {
  color: #3b3b3b;
  font-size: 2.5em;
}

.header p {
  color: #7a7a7a;
  font-size: 1.2em;
}

.carousel {
  margin-bottom: 20px;
}

.carousel-item {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #ffffff;
  font-size: 2em;
  height: 300px;
  background-color: #409eff;
}

.info-section {
  margin-bottom: 20px;
}

.el-col {
  text-align: center;
}

.demo-collapse {
  background-color: #f5f7fa;
  margin-top: 20px;
}

.statistic-title {
  display: inline-flex;
  align-items: center;
  font-weight: bold;
  color: #333;
}

.footer {
  text-align: center;
  margin-top: 40px;
  color: #7a7a7a;
}
</style>