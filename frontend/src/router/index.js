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
        path: '/read/:id', // 在路径中直接定义参数
        name: 'Read',
        component: () => import("../views/Read.vue"),
        props: true  // 使组件能够通过 props 接收路由参数
    }

    
];

// 创建路由实例
const router = createRouter({
    history: createWebHistory(),
    routes, 
});

export default router;
