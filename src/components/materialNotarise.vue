<script setup>
import { ref, reactive, onMounted } from 'vue';
import baseUrl from '../assets/apilink.json';
import axios from 'axios';
import { useMaterialStore, useHeightStore } from '../stores/counter';
// 循环表单中的内容
const materials = useMaterialStore().materials
// const materials = reactive([
//     { material: ref(''), quantity: ref(''), lot: ref(''), POV: ref('') }
// ])

// 新增项目
const addMaterial = () => {
    materials.push({ material: ref(''), quantity: ref(''), lot: ref(''), POV: ref('') })
}

// 删除项目
const removematerial = (item) => {
    const index = materials.indexOf(item)
    if (index !== -1) {
        materials.splice(index, 1)
    }
}

// 存放自动补全的物料名称
const materialList = ref([])

// 选择或根据输入提示物料名称
const querySearchMaterialsName = (queryString, cb) => {
    const results = queryString
        ? materialList.value.filter(createFilter(queryString))
        : materialList.value
    // call callback function to return suggestions
    cb(results)
}

// 根据输入显示剩余符合的自动补全列表
const createFilter = (queryString) => {
    return (restaurant) => {
        return (
            restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
        )
    }
}

// 存放获取焦点的临时设备编号
const templist = ref([])
const focusItem = ref()
const focusNum = (equipName) => {
    focusItem.value = equipName
}

// 根据设备名称更改设备编号自动补全内容
const querySearchMaterialNum = (queryString, cb) => {
    // 清除上一次选择的遗留选项
    templist.value = []
    // 获取设备对应编号列表
    materialList.value.forEach(obj => {
        if (obj.value === focusItem.value) {
            templist.value = obj.lot
        }
    })
    // 提供列表
    const results = queryString
        ? templist.value.filter(createFilter(queryString))
        : templist.value
    // call callback function to return suggestions
    cb(results)
}
//  选择批号时自动填充有效期
const autoFill = (item) => {
    templist.value.forEach(obj => {
        if (obj.value === item.lot) {
            item.POV = obj.POV
        }
    })
}

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

// 先搜索有几种物料名称
const materialNameMap = new Map()

const getMaterialNameMap = async () => {
    severData.forEach((item) => {
        materialNameMap.set(item['material_name'], 1)
    })
    // console.log(EquipmentNameMap)
}

const loadMaterialName = async () => {
    let res = []
    for (let [key, value] of materialNameMap) {
        let tempItem = { value: key, lot: [] }
        severData.forEach((item) => {
            if (item['material_name'] === key) {
                tempItem.lot.push({ value: item.material_lot, POV: item.material_EOV })
            }
        })
        res.push(tempItem)
    }
    return res
    // return [
    //     { value: '50mL离心管', lot: [{ value: '06023601', POV: '2028-02-28' }, { value: '06023061', POV: '2028-05-28' }] },
    //     { value: '250mL离心管', lot: [{ value: '298023601', POV: '2025-10-25' }] },
    //     { value: '10mL移液管', lot: [{ value: 'BB03004', POV: '2027-03' }] },
    //     { value: '25mL移液管', lot: [{ value: 'BB06005', POV: '2027-03' }] },
    // ]
}

onMounted(async () => {
    await getSeverData()
    await getMaterialNameMap()
    materialList.value = await loadMaterialName()
    // console.log(getMaterialUrl)

})

// 提交数据

</script>

<template>
    <el-scrollbar class="pcWeb" :height="useHeightStore().scrollbarHeight">
        <el-form class="material" :model="materials">
            <el-form-item class="materialItem" v-for="(item, index) in materials" :key="index">
                <nut-cell>
                    <el-autocomplete :fetch-suggestions="querySearchMaterialsName" clearable placeholder="物料名称"
                        v-model="item.material">
                    </el-autocomplete>
                    <el-input class="materialNumber" v-model="item.quantity" placeholder="数量" />
                    <el-autocomplete :fetch-suggestions="querySearchMaterialNum" clearable placeholder="物料批号"
                        @focus="focusNum(materials[index].material)" v-model="item.lot"
                        @select="autoFill(materials[index])">
                    </el-autocomplete>

                    <el-input class="materialNumber" v-model="item.POV" placeholder="有效期/复验期" />

                    <el-button type="danger" round @click="removematerial(item)">删除</el-button>
                </nut-cell>
            </el-form-item>
            <el-button type="primary" @click="addMaterial">+</el-button>
        </el-form>
    </el-scrollbar>

    <!-- 以下是移动端UI -->
    <nut-form class="mobileWeb">
        <nut-form-item v-for="(item, index) in materials" :key="index">
            <nut-cell size="large">
                <nut-input v-model="item.material" placeholder="物料名称"></nut-input>
            </nut-cell>

            <nut-cell size="large">
                <nut-input v-model="item.quantity" placeholder="数量"></nut-input>
            </nut-cell>

            <nut-cell size="large">
                <nut-input v-model="item.lot" placeholder="物料批号"></nut-input>
            </nut-cell>

            <nut-cell size="large">
                <nut-input v-model="item.POV" placeholder="有效期/复验期"></nut-input>
            </nut-cell>

            <nut-cell size="large">
                <nut-button type="danger" round @click="removematerial(item)">删除</nut-button>
            </nut-cell>
        </nut-form-item>
        <nut-button size="large" type="success" @click="addMaterial">增加条目</nut-button>
    </nut-form>
</template>

<style>
.titleName {
    text-align: center;
}

.infoInput {
    text-align: center;
}

.materialNumber {
    width: 180px;
}
</style>