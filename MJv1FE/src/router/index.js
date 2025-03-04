// router/index.js  
import { createRouter, createWebHistory } from 'vue-router';
import Customer from '@/components/Customer.vue';
import Room from '@/components/Room.vue';
import Employee from '@/components/Employee.vue';
import Supplies from '@/components/Supplies.vue';
import Home from '@/components/Home.vue';


const routes = [
    {
        path: '/customer',
        name: 'Customer',
        component: Customer, // 确保这个组件存在  
    },
    {
        path: '/home',
        name: 'Home',
        component: Home,
    },
    {
        path: '/supplies',
        name: 'Supplies',
        component: Supplies,
    },
    {
        path: '/room',
        name: 'Room',
        component: Room,
    },
    {
        path: '/employee',
        name: 'Employee',
        component: Employee,
    },
    { path: '/', redirect: '/home' },  // 默认重定向到首页  
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;