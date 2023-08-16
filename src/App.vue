<script setup>
import { RouterView, useRouter } from 'vue-router'
import { reactive, ref } from 'vue';
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

const router = useRouter()

// 移动端导航内容
const mobileNavVisible = ref(false)

const navList = reactive([
  {
    id:1,
    text: '细胞计数',
    path: '/cellCounting'
  },
  {
    id:2,
    text: '物料确认',
    path: '/materialNotarise'
  },
  {
    id:3,
    text: '设备确认',
    path: '/equipmentNotarise'
  },
])

const SelectedRouter = (value) => {
  // console.log(value.item.path)
  router.push({path: value.item.path})
}
</script>

<template>
  <el-row class="pcHeadBox"></el-row>
  <el-row class="mainBox pcWeb">
    <el-col class="sideBox" :span="3">
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
        <el-menu-item index="/getReport">
          查看记录
        </el-menu-item>
        <el-menu-item index="/addMaterial">
          新增物料
        </el-menu-item>
        <el-menu-item index="/addEquipment">
          新增设备
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col class="showBox" :span="21">
      <RouterView></RouterView>
      <el-row class="footer">
        <el-button class="pcWeb" type="primary" @click="upload">上传</el-button>
      </el-row>
    </el-col>
  </el-row>
  <!-- 以下是移动端页面 -->
  <nut-fixed-nav class="mobileWeb" type="left" :position="{ top: '140px' }" v-model:visible="mobileNavVisible" :nav-list="navList" @selected="SelectedRouter"/>
  <nut-row class="mainBox mobileWeb">
    <nut-col class="showBox" :span="24">
      <RouterView></RouterView>
    </nut-col>
    
    <nut-button class="mobileWeb uploadButton" type="info" @click="upload">上传</nut-button>
  </nut-row>
</template>

<style>
.footer {
  justify-content: center;
}


@media (min-width: 768px) {
    .mobileWeb {
        display: none;
        --nut-input-font-size: 40px;
    }
}

@media (max-width: 767px) {
    .pcWeb {
        display: none;
    }

}
</style>
