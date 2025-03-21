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
import StaffManage from "@/views/StaffManage.vue";
import Test from "@/views/Test.vue";

const routes = [
  {
    path: "/customer",
    name: "顾客管理",
    component: Customer, // 确保这个组件存在
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
  },
  {
    path: "/roomManage",
    name: "房间管理",
    component: RoomManage,
  },
  {
    path: "/employee",
    name: "员工管理",
    component: Employee,
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
    path: "/staffManage",
    name: "职员管理",
    component: StaffManage,
  },
  {
    path: "/test",
    name: "Test",
    component: Test,
  },
  { path: "/", redirect: "/home" }, // 默认重定向到首页
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 受保护的路由列表
const protectedRoutesFromManager = [
  "/customer",
  "/supplies",
  "/employee",
  "/roomManage",
];

const protectedRoutesFromAdmin = ["/staffManage"];

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  if (protectedRoutesFromManager.includes(to.path)) {
    if (userStore.role !== "manager") {
      ElMessage.error("您没有权限访问此页面。");
      return next({ path: "/home" });
    }
  }

  if (protectedRoutesFromAdmin.includes(to.path)) {
    if (userStore.role !== "admin") {
      ElMessage.error("您没有权限访问此页面。");
      return next({ path: "/home" });
    }
  }
  
  next();
});

export default router;
