<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <el-row class="pcHeadBox" :span="24"></el-row>
  <el-row class="mainBox" :span="24">
    <el-col class="sideBox" :span="0" :md="3">
      <el-menu router="true">
        <el-menu-item index="/addMaterial">
          新增物料
        </el-menu-item>
        <el-menu-item index="/addEquipment">
          新增设备
        </el-menu-item>
        <el-menu-item index="/cellCounting">
          细胞计数
        </el-menu-item>
        <el-menu-item index="/materialNotarise">
          物料确认
        </el-menu-item>
        <el-menu-item index="/equipmentNotarise">
          设备确认
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col class="showBox" :span="24" :md="19">
      <RouterView></RouterView>
    </el-col>
  </el-row>
</template>

<style scoped></style>
