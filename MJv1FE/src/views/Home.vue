<template>
  <div class="home-page" :class="{ dark: isDark }">
    <main class="main-container">
      <header class="header">
        <h1>美佳公寓智能管理平台</h1>
        <p>高效、便捷、智能的公寓管理解决方案</p>
      </header>

      <el-carousel indicator-position="outside" trigger="click" class="carousel">
        <el-carousel-item v-for="item in carouselItems" :key="item.id">
          <h3 class="carousel-item">{{ item.text }}</h3>
        </el-carousel-item>
      </el-carousel>
    </main>

    <!-- 数据卡片 -->
    <div class="dashboard-cards">
      <el-row :gutter="20">
        <el-col v-for="(stat, index) in stats" :key="index" :xs="24" :sm="12" :md="6">
          <div class="stat-card" :class="`theme-${index % 4}`" @mouseenter="handleCardHover(index)">
            <div class="card-icon">
              <component :is="stat.icon" class="icon" />
            </div>
            <div class="card-content">
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-value">
                <count-up :end-val="stat.value" :options="countUpOptions" />
                <span v-if="stat.suffix" class="suffix">{{ stat.suffix }}</span>
              </div>
              <div class="stat-trend">
                <el-icon :color="stat.trendColor">
                  <CaretTop v-if="stat.trend === 'up'" />
                  <CaretBottom v-else />
                </el-icon>
                <span :style="{ color: stat.trendColor }">{{ stat.trendValue }}</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { markRaw, ref } from 'vue';
import { useDark } from '@vueuse/core';
import { User, TrendCharts, Money, ChatRound } from '@element-plus/icons-vue'
import CountUp from 'vue-countup-v3'

const carouselItems = ref([
  { id: 1, text: '智能管理，便捷生活' },
  { id: 2, text: '高效服务，满意体验' },
  { id: 3, text: '全面监控，安全无忧' },
  { id: 4, text: '数据分析，决策支持' },
]);


// 统计数据
const source = ref(0);

source.value = 172000;

// 深色主题切换
const isDark = useDark(); // 检测当前是否为深色模式

// 统计卡片数据
const stats = ref([
  {
    icon: markRaw(User), // 使用 markRaw 标记组件对象
    title: '今日活跃用户',
    value: 1423,
    trend: 'up',
    trendValue: '+12.5%',
    trendColor: '#52c41a',
    suffix: '人'
  },
  {
    icon: markRaw(TrendCharts), // 使用 markRaw 标记组件对象
    title: '本月出租率',
    value: 86.7,
    trend: 'down',
    trendValue: '-3.2%',
    trendColor: '#f5222d',
    suffix: '%'
  },
  {
    icon: markRaw(Money), // 使用 markRaw 标记组件对象
    title: '年度总营收',
    value: 256.8,
    trend: 'up',
    trendValue: '+24.7%',
    trendColor: '#52c41a',
    suffix: '亿'
  },
  {
    icon: markRaw(ChatRound), // 使用 markRaw 标记组件对象
    title: '用户满意度',
    value: 120,
    trend: 'up',
    trendValue: '+0.8%',
    trendColor: '#52c41a',
    suffix: '分'
  }
])

// CountUp配置
const countUpOptions = {
  duration: 2,
  separator: ',',
  decimalPlaces: 1
}

// 卡片悬停效果
const handleCardHover = (index: number) => {
  // 可以添加额外交互逻辑
}
</script>