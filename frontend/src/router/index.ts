import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'start',
      component: import('../views/HomeView.vue')
    },
    {
      path: '/week',
      name: 'uge',
      component: () => import('../views/WeekView.vue')
    },
    {
      path: '/coworker',
      name: 'medarbejder',
      component: () => import('../views/CoworkerView.vue')
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('../views/UploadView.vue')
    }
  ]
})

export default router
