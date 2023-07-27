<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <el-row class="pcHeadBox" :span="24"></el-row>
  <el-row class="mainBox" :span="24">
    <el-col class="sideBox" :span="0" :md="3"></el-col>
    <el-col class="showBox" :span="24" :md="19"></el-col>
  </el-row>
</template>

<style scoped></style>
