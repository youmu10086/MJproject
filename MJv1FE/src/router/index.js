import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/store/userStore";
import { ElMessage } from "element-plus";

const Customer = () => import("@/views/Customer.vue");
const Employee = () => import("@/views/Employee.vue");
const Supplies = () => import("@/views/Supplies.vue");
const Home = () => import("@/views/Home.vue");
const OnlineService = () => import("@/views/OnlineService.vue");
const ReviewsFeedback = () => import("@/views/ReviewsFeedback.vue");
const ReservationManage = () => import("@/views/ReservationManage.vue");
const userManage = () => import("@/views/userManage.vue");
const Test = () => import("@/views/Test.vue");
const Room = () => import("@/views/Room.vue");

const routes = [
  {
    path: "/customer",
    name: "顾客管理",
    component: Customer,
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
    path: "/room",
    name: "房间管理",
    component: Room,
    meta: { requiresAuth: true, requiredRole: ["manager", "customer", "guest"] },
  },
  {
    path: "/employee",
    name: "员工管理",
    component: Employee,
    meta: { requiresAuth: true, requiredRole: "manager" },
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
  {
    path: "/test",
    name: "Test",
    component: Test,
  },
  { path: "/", redirect: "/home" },
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
    if (to.meta.requiredRole && !to.meta.requiredRole.includes(userStore.role)) {
      ElMessage.error("您没有访问该页面的权限");
      return next(from.path || "/home");
    }
  }

  next();
});

export default router;
