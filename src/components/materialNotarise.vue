<script setup>
import { ref, reactive, onMounted } from 'vue';

// 循环表单中的内容
const materials = reactive([
    { material: ref(''), quantity: ref(''), lot: ref(''), POV: ref('') }
])

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

const loadMaterialName = () => {
    return [
        { value: '50mL离心管', lot: [{ value: '06023601', POV: '2028-02-28' }, { value: '06023061', POV: '2028-05-28' }] },
        { value: '250mL离心管', lot: [{ value: '298023601', POV: '2025-10-25' }] },
        { value: '10mL移液管', lot: [{ value: 'BB03004', POV: '2027-03' }] },
        { value: '25mL移液管', lot: [{ value: 'BB06005', POV: '2027-03' }] },
    ]
}

onMounted(() => {
    materialList.value = loadMaterialName()
})
</script>

<template>
    <el-form class="material" :model="materials">
        <el-row class="titleBox">
            <el-col class="titleName" :span="4">
                <el-text class="equipName">物料名称</el-text>
            </el-col>
            <el-col class="titleName" :span="2">
                <el-text class="equipNum">数量</el-text>
            </el-col>
            <el-col class="titleName" :span="10">
                <el-text class="availability">批号</el-text>
            </el-col>
            <el-col class="titleName" :span="4">
                <el-text class="availability">有效期/复验期</el-text>
            </el-col>
        </el-row>
        <el-row class="writeBox">
            <el-col :span="24">
                <el-form-item class="materialItem" v-for="(item, index) in materials" :key="index">
                    <el-col class="infoInput" :span="4">
                        <el-autocomplete :fetch-suggestions="querySearchMaterialsName" clearable placeholder="请输入物料名称"
                            v-model="item.material">
                        </el-autocomplete>
                    </el-col>
                    <el-col class="infoInput" :span="2">
                        <el-input v-model="item.quantity" placeholder="请输入数量" />
                    </el-col>
                    <el-col class="infoInput" :span="10">
                        <el-autocomplete :fetch-suggestions="querySearchMaterialNum" clearable placeholder="请输入物料批号"
                            @focus="focusNum(materials[index].material)" v-model="item.lot" @select="autoFill(materials[index])">
                        </el-autocomplete>
                    </el-col>
                    <el-col class="infoInput" :span="4">
                        <el-input v-model="item.POV" placeholder="请输入有效期/复验期" />
                    </el-col>
                    <el-col class="infoInput" :span="3">
                        <el-button type="danger" round @click="removematerial(item)">删除</el-button>
                    </el-col>
                </el-form-item>
            </el-col>
            <el-col :span="3">
                <el-button type="primary" @click="addMaterial">+</el-button>
            </el-col>
        </el-row>
        {{ materials }}
    </el-form>
</template>

<style>
.titleName {
    text-align: center;
}

.infoInput {
    text-align: center;
}
</style>