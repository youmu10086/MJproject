import { createRouter, createWebHistory } from "vue-router";
import Customer from "@/views/Customer.vue";
import RoomManage from "@/views/RoomManage.vue";
import Employee from "@/views/Employee.vue";
import Supplies from "@/views/Supplies.vue";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import RoomReservation from "@/views/RoomReservation.vue";
import OnlineService from "@/views/OnlineService.vue";
import ReviewsFeedback from "@/views/ReviewsFeedback.vue";
import ReservationManage from "@/views/ReservationManage.vue";
import Test from "@/views/Test.vue";

const routes = [
  {
    path: "/customer",
    name: "Customer",
    component: Customer, // 确保这个组件存在
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
  },
  {
    path: "/supplies",
    name: "Supplies",
    component: Supplies,
  },
  {
    path: "/roomManage",
    name: "RoomManage",
    component: RoomManage,
  },
  {
    path: "/employee",
    name: "Employee",
    component: Employee,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/roomReservation",
    name: "RoomReservation",
    component: RoomReservation,
  },
  {
    path: "/onlineService",
    name: "OnlineService",
    component: OnlineService,
  },
  {
    path: "/reservationManage",
    name: "ReservationManage",
    component: ReservationManage,
  },
  {
    path: "/reviewsFeedback",
    name: "ReviewsFeedback",
    component: ReviewsFeedback,
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

// // 在 router/index.ts 中添加
// router.beforeEach((to, from, next) => {
//   // 检查用户是否登录，这里只是一个示例，你应该有实际的逻辑
//   const isLoggedIn = false; // 替换为实际的登录状态检查

//   if (to.path === "/login" || isLoggedIn) {
//     next();
//   } else {
//     next("/login");
//   }
// });
export default router;
