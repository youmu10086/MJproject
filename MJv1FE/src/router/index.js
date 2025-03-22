import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/store/userStore";
import { ElMessage } from "element-plus";

import Customer from "@/views/Customer.vue";
import RoomManage from "@/views/RoomManage.vue";
import Employee from "@/views/Employee.vue";
import Supplies from "@/views/Supplies.vue";
import Home from "@/views/Home.vue";
import RoomReservation from "@/views/RoomReservation.vue";
import OnlineService from "@/views/OnlineService.vue";
import ReviewsFeedback from "@/views/ReviewsFeedback.vue";
import ReservationManage from "@/views/ReservationManage.vue";
import userManage from "@/views/userManage.vue";
// import Test from "@/views/Test.vue";

const routes = [
  {
    path: "/customer",
    name: "顾客管理",
    component: Customer, // 确保这个组件存在
    meta: { requiresAuth: true, requiredRole: "manager" },
  },
  {
    path: "/home",
    name: "主页面",
    component: Home,
  },
  {
    path: "/supplies",
    name: "住房用品管理",
    component: Supplies,
    meta: { requiresAuth: true, requiredRole: "manager" },
  },
  {
    path: "/roomManage",
    name: "房间管理",
    component: RoomManage,
    meta: { requiresAuth: true, requiredRole: "manager" },
  },
  {
    path: "/employee",
    name: "员工管理",
    component: Employee,
    meta: { requiresAuth: true, requiredRole: "manager" },
  },
  {
    path: "/roomReservation",
    name: "预订房间",
    component: RoomReservation,
  },
  {
    path: "/onlineService",
    name: "在线服务",
    component: OnlineService,
  },
  {
    path: "/reservationManage",
    name: "预订管理",
    component: ReservationManage,
  },
  {
    path: "/reviewsFeedback",
    name: "反馈",
    component: ReviewsFeedback,
  },
  {
    path: "/userManage",
    name: "用户管理",
    component: userManage,
    meta: { requiresAuth: true, requiredRole: "admin" },
  },
  // {
  //   path: "/test",
  //   name: "Test",
  //   component: Test,
  // },
  { path: "/", redirect: "/home" }, // 默认重定向到首页
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  // 需要身份验证的路由
  if (to.meta.requiresAuth) {
    // 未登录状态
    if (!userStore.isLoggedIn) {
      userStore.loginDialogVisible = true;
      return next(false);
    }

    // 已登录但需要更新角色状态
    if (userStore.role === "guest") {
      try {
        const success = await userStore.fetchUserRole();
        if (!success) {
          ElMessage.error("获取用户权限失败");
          return next("/home");
        }
      } catch (error) {
        return next("/login");
      }
    }

    // 角色权限验证
    if (to.meta.requiredRole && userStore.role !== to.meta.requiredRole) {
      ElMessage.error("您没有访问该页面的权限");
      return next(from.path || "/home");
    }
  }

  next();
});

export default router;
