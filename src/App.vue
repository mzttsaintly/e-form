<script setup>
import { RouterView, useRouter } from 'vue-router'
import { reactive, ref } from 'vue';
import { useCellCountindStore, useEquipmentStore, useMaterialStore, useSideBarStore, useLoginStore } from './stores/counter';
import baseUrl from './assets/apilink.json';
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import headVue from './views/headVue.vue';
// 组合需上传的数据
const uploadData = reactive({
  uploadMaterial: useMaterialStore().materials,
  uploadEquipment: useEquipmentStore().equipment,
  uploadCells: useCellCountindStore().cellCounted
})

// 从服务器获得token
const tokenStore = useLoginStore()
// 生成的请求头
const gotHeaders = tokenStore.get_headers()

// 上传url
const uploadUrl = baseUrl['baseUrl'] + 'get_data'

// 上传数据的方法
const upload = () => {
  console.log(uploadData)
  axios.post(uploadUrl, uploadData, gotHeaders).then(
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
// 侧边栏状态
const sideBarState = useSideBarStore().sideBarState

// const mobileNavVisible = ref(false)

// const navList = reactive([
//   {
//     id: 1,
//     text: '细胞计数',
//     path: '/cellCounting'
//   },
//   {
//     id: 2,
//     text: '物料确认',
//     path: '/materialNotarise'
//   },
//   {
//     id: 3,
//     text: '设备确认',
//     path: '/equipmentNotarise'
//   },
//   {
//     id: 4,
//     text: '查看报告',
//     path: '/getReport'
//   },
//   {
//     id: 5,
//     text: '登录',
//     path: '/login'
//   },
// ])

// const SelectedRouter = (value) => {
//   // console.log(value.item.path)
//   router.push({ path: value.item.path })
// }
</script>

<template>
  <el-row class="pcHeadBox">
    <headVue></headVue>
  </el-row>

  <el-row class="mainBox pcWeb">
    <el-col class="sideBox" :span="3">
      <el-menu router="true" default-active="/login">
        <!-- <el-menu-item index="/login">
          用户登录
        </el-menu-item> -->
        <el-menu-item index="/cellCounting">
          细胞计数
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
          物料管理
        </el-menu-item>
        <el-menu-item index="/addEquipment">
          设备管理
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col class="showBox" :span="21">
      <RouterView></RouterView>
      <nut-divider></nut-divider>
      <el-row class="footer">
        <el-button class="pcWeb" type="primary" @click="upload">上传</el-button>
      </el-row>
    </el-col>
  </el-row>
  <!-- 以下是移动端页面 -->
  <!-- <nut-drag direction="y" :style="{ left: '0px', bottom: '240px' }">
    <nut-fixed-nav class="mobileWeb" type="left" :position="{ top: '140px' }" v-model:visible="mobileNavVisible"
      :nav-list="navList" @selected="SelectedRouter">
      <template v-slot:btn>
        <Retweet color="#fff" />
        <span class="text">{{ mobileNavVisible ? '关闭菜单' : '打开菜单' }}</span>
      </template>
    </nut-fixed-nav>
  </nut-drag> -->

  <!-- 移动端侧边栏 -->
  <nut-popup class="mobileWeb" position="left" v-model:visible="sideBarState.show"
    :style="{ width: sideBarState.width, height: sideBarState.height }">
    <nut-side-navbar-item ikey="1" title="细胞计数" @click="router.push({ path: '/cellCounting' })"></nut-side-navbar-item>

    <nut-side-navbar-item ikey="2" title="物料确认" @click="router.push({ path: '/materialNotarise' })"></nut-side-navbar-item>

    <nut-side-navbar-item ikey="3" title="设备确认" @click="router.push({ path: '/equipmentNotarise' })"></nut-side-navbar-item>

    <nut-side-navbar-item ikey="4" title="查看记录" @click="router.push({ path: '/getReport' })"></nut-side-navbar-item>

    <nut-side-navbar-item ikey="5" title="物料管理" @click="router.push({ path: '/addMaterial' })"></nut-side-navbar-item>

    <nut-side-navbar-item ikey="6" title="设备管理" @click="router.push({ path: '/addEquipment' })"></nut-side-navbar-item>
  </nut-popup>

  <nut-row class="mainBox mobileWeb">
    <nut-col class="showBox" :span="24">
      <RouterView></RouterView>
      <nut-divider></nut-divider>
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
