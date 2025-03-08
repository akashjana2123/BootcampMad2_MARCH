import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserSignup from '@/auth/UserSignup.vue'
import LoginUser from '@/auth/LoginUser.vue'
import CategoryManage from '@/components/CategoryManage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/usersignup',
    name: 'UserSignup',
    component: UserSignup
  },
  {
    path: '/login',
    name: 'AppLogin',
    component: LoginUser
  },
  {
    path: '/category',
    name: 'CategoryManage',
    component: CategoryManage
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
