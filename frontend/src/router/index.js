import { createRouter, createWebHistory } from 'vue-router';

// 定义路由
const routes = [

    {
    path: '/register',
    name: 'Register',
    component: () =>import("../views/Register.vue")
    },
    {
        path:'/',
        name:"Login",
        component: () =>import("../views/Login.vue")
    },
    {
        path:'/main',
        name:"Main",
        component: () =>import("../views/Main.vue")
    },
    {
        path:'/read',
        name:"Read",
        component: () =>import("../views/Read.vue")
    }
    
];

// 创建路由实例
const router = createRouter({
    history: createWebHistory(),
    routes, 
});

export default router;
