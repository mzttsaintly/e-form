<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import baseUrl from '../assets/apilink.json'

import { useLoginStore, useHeightStore } from '../stores/counter';

// 从服务器获得token
const tokenStore = useLoginStore()
// 生成的请求头
const gotHeaders = tokenStore.get_headers()

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
    axios.post(addMaterialUrl, addMaterial, gotHeaders).then(
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
const severData = reactive([])

// 从服务器获取数据
const getSeverData = async () => {
    await axios.post(getMaterialUrl).then(
        (response) => {
            severData.length = 0;
            response.data.forEach((item) => {
                severData.push(item)
            })
            // severData = response.data;
            console.log(severData)
        }
    ).catch((err) => {
        ElMessageBox.alert(err, '服务器错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}

// 删除条目
const del_url = baseUrl['baseUrl'] + 'use_del_material'

// 删除前确认
const verifyDelMaterial = async (id) => {
    ElMessageBox.confirm('确定删除该条目？', '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(
        async () => {
            await delMaterial(id)
        }
    )
}

const delMaterial = async (id) => {
    await axios.post(del_url, { 'id': id }, gotHeaders).then(
        (response) => {
            ElMessage(response.data)
        }
    ).catch((err) => {
        console.log(err)
        ElMessage(err)
    })
    await getSeverData()
}

onMounted(async () => {
    await getSeverData()
})
</script>

<template>
    <nut-tabs v-model="materialTabsStates">
        <nut-tab-pane title="物料信息查询">
            <el-scrollbar :height="useHeightStore().scrollbarHeight">
                <el-table :data="severData">
                    <el-table-column prop="id" label="ID" sortable></el-table-column>
                    <el-table-column prop="material_name" label="物料名称" sortable></el-table-column>
                    <el-table-column prop="material_lot" label="物料批号" sortable></el-table-column>
                    <el-table-column prop="material_EOV" label="有效期/复验期" sortable></el-table-column>
                    <el-table-column label="操作">
                        <template v-slot="operation_material">
                            <el-tooltip content="修改内容">
                                <el-button @click="console.log(operation_material.row.id)">
                                    <el-icon>
                                        <EditPen />
                                    </el-icon>
                                </el-button>
                            </el-tooltip>

                            <el-tooltip content="删除条目">
                                <el-button type="danger" @click="verifyDelMaterial(operation_material.row.id)"><el-icon>
                                        <CloseBold />
                                    </el-icon></el-button>
                            </el-tooltip>

                            <!-- {{ operation_material.row.id }} -->
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>

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