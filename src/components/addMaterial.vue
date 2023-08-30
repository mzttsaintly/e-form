<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import baseUrl from '../assets/apilink.json'

const addMaterial = reactive([{
    material_name: ref(''),
    material_lot: ref(''),
    material_EOV: ref('')
}])

const addM = () => {
    addMaterial.push({
        material_name: ref(''),
        material_lot: ref(''),
        material_EOV: ref('')
    })
}

// 提交数据
const addMaterialUrl = baseUrl['baseUrl'] + 'add_Material'

const pushMaterial = () => {
    axios.post(addMaterialUrl, addMaterial).then(
        function (response) {
            ElMessageBox.alert(response.data, '提交结果', {
                confirmButtonText: 'OK',
            })
        }
    ).catch(function (err) {
        ElMessageBox.alert(err, '服务器错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}

// 选项卡参数
const materialTabsStates = ref(0)

// 获取物料列表链接
const getMaterialUrl = baseUrl['baseUrl'] + 'queryMaterial'

// 临时存储从服务器获取的数据
let severData = []

// 从服务器获取数据
const getSeverData = async () => {
    await axios.post(getMaterialUrl).then(
        (response) => {
            severData = response.data;
            // console.log(severData)
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
    <nut-tabs v-model="materialTabsStates">
        <nut-tab-pane title="物料信息查询">
            
        </nut-tab-pane>

        <nut-tab-pane title="物料信息录入">
            <el-form :model="addMaterial">
                <el-form-item v-for="(item, index) in addMaterial" :key="index">
                    <el-tag>{{ index + 1 }}</el-tag>
                    <el-input v-model="item.material_name"><template #prepend>物料名称</template></el-input>
                    <el-input v-model="item.material_lot"><template #prepend>物料批号</template></el-input>
                    <el-input v-model="item.material_EOV"><template #prepend>有效期/复验期</template></el-input>
                </el-form-item>
                <el-button type="primary" @click="addM">+</el-button>
            </el-form>
            <el-button @click="pushMaterial" type="info">提交</el-button>
        </nut-tab-pane>
    </nut-tabs>
</template>