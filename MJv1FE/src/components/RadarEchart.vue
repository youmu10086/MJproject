<template>
  <v-chart :option="chartOption" style="width: 300px; height: 300px;" :theme="isDark ? 'dark' : 'light'" />
</template>

<script setup>
defineOptions({ name: 'RadarEchart' });
import { useDark } from '@vueuse/core';

const { isDark } = useDark();


const chartOption = {
  tooltip: {},
  legend: {
    orient: 'vertical', // 垂直排列
    left: '15%', // 距离左侧 5%
    top: '20%', // 距离顶部 20%，位于标题下方
    textStyle: {
      fontSize: 10, // 缩小图例字体大小
    },
    data: ['当前评分', '历史平均分'],
  },
  radar: {
    radius: '100%', // 设置雷达图的半径为容器的 100%
    indicator: [
      { name: '卫生状况', max: 10 },
      { name: '设施设备', max: 10 },
      { name: '服务响应', max: 10 },
      { name: '安全保障', max: 10 },
      { name: '性价比', max: 10 },
    ],
  },
  series: [
    {
      name: '评分对比',
      type: 'radar',
      data: [
        { value: [8, 9, 10, 8.6, 4], name: '当前评分' },
        { value: [8, 9, 10, 8.6, 6], name: '历史平均分' },
      ],
    },
  ],
};
</script>