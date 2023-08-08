<script setup>
import { RouterView } from 'vue-router'
import { reactive } from 'vue';
import { useCellCountindStore, useEquipmentStore, useMaterialStore } from './stores/counter';
import baseUrl from './assets/apilink.json';
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
// 组合需上传的数据
const uploadData = reactive({
  uploadMaterial: useMaterialStore().materials,
  uploadEquipment: useEquipmentStore().equipment,
  uploadCells: useCellCountindStore().cellCounted
})

// 上传url
const uploadUrl = baseUrl['baseUrl'] + 'get_data'

// 上传数据的方法
const upload = () => {
  console.log(uploadData)
  axios.post(uploadUrl, uploadData).then(
    (response) => {
      console.log(response.data)
      ElMessageBox.alert(response.data, '上传结果', {
        confirmButtonText: '确认',
        callback: (action) => {
          ElMessage({
            type: 'success',
            message: `${action}`
          })
        }
      })
    }
  ).catch((err) => {
    ElMessageBox.alert(err, '服务器错误', {
      confirmButtonText: 'OK',
    })
    console.log(err)
  })
}
</script>

<template>
  <el-row class="pcHeadBox"></el-row>
  <el-row class="mainBox">
    <el-col class="sideBox" :span="3" :md="3">
      <el-menu router="true">
        <el-menu-item index="/cellCounting">
          <el-text>细胞计数</el-text>
        </el-menu-item>
        <el-menu-item index="/materialNotarise">
          物料确认
        </el-menu-item>
        <el-menu-item index="/equipmentNotarise">
          设备确认
        </el-menu-item>
        <el-menu-item index="/addMaterial">
          新增物料
        </el-menu-item>
        <el-menu-item index="/addEquipment">
          新增设备
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col class="showBox" :span="21" :md="21">
      <RouterView></RouterView>
      <el-row class="footer">
        <el-button type="primary" @click="upload">上传</el-button>
      </el-row>
    </el-col>
  </el-row>
</template>

<style scoped></style>
