import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/addMaterial',
      name: 'addMaterial',
      component: () => import('../components/addMaterial.vue')
    },
    {
      path: '/addEquipment',
      name: 'addEquipment',
      component: () => import('../components/addEquipment.vue')
    },
    {
      path: '/cellCounting',
      name: 'cellCounting',
      component: () => import('../components/cellCounting.vue')
    },
    {
      path: '/materialNotarise',
      name: 'materialNotarise',
      component: () => import('../components/materialNotarise.vue')
    },
    {
      path: '/equipmentNotarise',
      name: 'equipmentNotarise',
      component: () => import('../components/equipmentNotarise.vue')
    },
    {
      path: '/getReport',
      name: 'getReport',
      component: () => import('../components/getReport.vue')
    },
  ]
})

export default router
