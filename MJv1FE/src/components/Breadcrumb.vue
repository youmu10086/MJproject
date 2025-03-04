<template>
  <el-breadcrumb :separator-icon="ArrowRight">
    <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index">
      <router-link :to="item.path">{{ item.name }}</router-link>
    </el-breadcrumb-item>
  </el-breadcrumb>
  <el-breadcrumb :separator-icon="ArrowRight" class="no-select">
    <el-breadcrumb-item :to="{ path: '<' }">首页</el-breadcrumb-item>
    <el-breadcrumb-item>入住人员管理</el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script>
export default {
  computed: {
    breadcrumbs() {
      const routes = this.$route.matched; // 获取当前路由的全部嵌套路由  
      return routes.map(route => ({
        name: route.meta?.title || route.name,
        path: route.path,
      }));
    },
  },
};
</script>
