import { createRouter, createWebHistory } from 'vue-router';
import loginVue from '../components/login.vue';
import addEquipmentVue from '../components/addEquipment.vue';
import addMaterialVue from '../components/addMaterial.vue';
import cellCountingVue from '../components/cellCounting.vue';
import materialNotariseVue from '../components/materialNotarise.vue';
import equipmentNotariseVue from '../components/equipmentNotarise.vue';
import getReportVue from '../components/getReport.vue';
import userInfoVue from '../components/userInfo.vue'
import { useLoginStore } from '../stores/counter';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: loginVue,
    },
    {
      path: '/addMaterial',
      name: 'addMaterial',
      component: addMaterialVue,
    },
    {
      path: '/addEquipment',
      name: 'addEquipment',
      component: addEquipmentVue,
    },
    {
      path: '/cellCounting',
      name: 'cellCounting',
      component: cellCountingVue,
    },
    {
      path: '/materialNotarise',
      name: 'materialNotarise',
      component: materialNotariseVue,
    },
    {
      path: '/equipmentNotarise',
      name: 'equipmentNotarise',
      component: equipmentNotariseVue,
    },
    {
      path: '/getReport',
      name: 'getReport',
      component: getReportVue,
    },
    {
      path: '/userInfo',
      name: 'userInfo',
      component: userInfoVue,
    }
  ]
})

router.beforeEach((to, from) => {
  const isLogin = useLoginStore().notarizeLogin()
  if (to.path === '/login') {
    if (isLogin) {
      return {path: '/userInfo'}
    }
  }
  if (to.path === '/userInfo') {
    if (isLogin === false) {
      return {path: '/login'}
    }
  }
})

export default router
