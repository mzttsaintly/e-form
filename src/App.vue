<script setup>
import { RouterLink, RouterView } from 'vue-router'

import equipmentNotarise from './components/equipmentNotarise.vue';
import materialNotarise from './components/materialNotarise.vue';
import cellCounting from './components/cellCounting.vue';
</script>

<template>
  <el-row class="pcHeadBox" :span="24"></el-row>
  <el-row class="mainBox" :span="24">
    <el-col class="sideBox" :span="0" :md="3"></el-col>
    <el-col class="showBox" :span="24" :md="19">
      <equipmentNotarise></equipmentNotarise>
      <br>
      <materialNotarise></materialNotarise>
      <br>
      <cellCounting></cellCounting>
    </el-col>
  </el-row>
</template>

<style scoped></style>
