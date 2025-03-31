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
    suffix: '万'
  },
  {
    icon: markRaw(ChatRound), // 使用 markRaw 标记组件对象
    title: '用户满意度',
    value: 98.5,
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

<style scoped lang="scss">
@use "sass:list";
.dashboard-cards {
  margin-top: 40px;

  .stat-card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    cursor: pointer;
    position: relative;
    overflow: hidden;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    .card-icon {
      width: 48px;
      height: 48px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(var(--primary-color), 0.1);
      margin-bottom: 20px;

      .icon {
        width: 24px;
        height: 24px;
        color: var(--primary-color);
      }
    }

    .stat-title {
      font-size: 0.95rem;
      color: var(--text-color);
      opacity: 0.8;
      margin-bottom: 8px;
    }

    .stat-value {
      font-size: 1.8rem;
      font-weight: 600;
      color: var(--text-color);
      display: flex;
      align-items: baseline;

      .suffix {
        font-size: 0.9rem;
        margin-left: 4px;
        opacity: 0.8;
      }
    }

    .stat-trend {
      margin-top: 12px;
      display: flex;
      align-items: center;
      font-size: 0.9rem;
      gap: 4px;
    }
  }

  // 不同卡片颜色主题
  @for $i from 0 through 3 {
    .theme-#{$i} {
      $colors: (
        #409eff,
        #67c23a,
        #e6a23c,
        #f56c6c
      );
    --theme-color: list.nth($colors, $i + 1);

    .card-icon {
      background: rgba(list.nth($colors, $i + 1), 0.1);

      .icon {
        color: list.nth($colors, $i + 1);
      }
    }
  }
}
}

:root {
  --background-color: #666666;
  --text-color: #333;
  --header-bg-color: #ffffff;
  --statistic-title-color: #333;
}

/* 深色主题 */
.dark {
  --background-color: #141414;
  --text-color: #ffffff;
  --header-bg-color: #333333;
  --statistic-title-color: #ffffff;
}

.home-page {
  font-family: 'Arial', sans-serif;
  padding: 20px;
  background-color: var(--background-color);
  color: var(--text-color);
  --carousel-item-bg-color: rgb(51.2, 126.4, 204);
}

.home-page.dark {
  --carousel-item-bg-color: #1e1e1e;
}

:deep(.el-carousel__item) {
  background: var(--carousel-item-bg-color);
  display: flex;
  justify-content: center;
  align-items: center;
  color: #ffffff;
  font-size: 2em;
  height: 280px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  /* 添加文字阴影，增加立体感 */
}


.header {
  text-align: center;
  margin-bottom: 20px;
  height: 180px;
  
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.header h1 {
  color: var(--text-color);
  font-size: 2.5em;
}

.header p {
  color: #7a7a7a;
  font-size: 1.2em;
}

.carousel {
  margin-bottom: 20px;
}

.info-section {
  margin-bottom: 20px;
}

.el-col {
  text-align: center;
}

.demo-collapse {
  background-color: var(--background-color);
  margin-top: 20px;
}

.statistic-title {
  display: inline-flex;
  align-items: center;
  font-weight: bold;
  color: var(--statistic-title-color);
}
</style>