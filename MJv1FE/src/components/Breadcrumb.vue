<template>
  <el-breadcrumb :separator-icon="ArrowRight">
    <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index">
      <router-link :to="item.path">{{ item.name }}</router-link>
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { ArrowRight } from '@element-plus/icons-vue';

const route = useRoute();

const breadcrumbs = computed(() => {
  const routes = route.matched; // 获取当前路由的全部嵌套路由  
  return routes.map(route => ({
    name: route.meta?.title || route.name,
    path: route.path,
  }));
});  
</script>