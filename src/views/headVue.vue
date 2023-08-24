<script setup>
import { HorizontalN, My2 } from '@nutui/icons-vue';
import { useSideBarStore } from '../stores/counter';
import {  useRouter } from 'vue-router'
const router = useRouter()
// 侧边栏开关
const handleClick = useSideBarStore().handleClick
</script>

<template>
    <nut-navbar class="pcWeb" title="快捷记录" @on-click-right="router.push({ path: '/login' })">
      <template #right>
      <My2 class="right" width="16px"></My2>
    </template>
    </nut-navbar>


  <!-- 移动端头部导航 -->
  <nut-navbar class="mobileWeb" title="快捷记录" @on-click-back="handleClick" @on-click-right="router.push({ path: '/login' })">
    <template #left>
      <HorizontalN class="left" width="16px"></HorizontalN>
    </template>

    <template #right>
      <My2 class="right" width="16px"></My2>
    </template>
  </nut-navbar>
</template>