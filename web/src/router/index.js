import { inject } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router'

import LoGin from '../views/LoGin.vue'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoGin
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true }  // 需要登录才能访问
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const store = inject('store'); // 使用 `inject` 函数，从 Vue 应用程序中获取 Vuex store 实例
  const loggedIn = store.state.loggedIn; // 读取存储在 Vuex store 中的变量
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/');  // 未登录，重定向到登录页面
  } else {
    next();  // 已登录，继续导航
  }
});

export default router
