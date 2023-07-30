<script setup>
import { ref, reactive, onMounted } from 'vue';

// 循环表单中的内容
const equipment = reactive([
    { equipName: ref(''), equipNum: ref(''), availability: ref() }
])

// 新增项目
const addEquipment = () => {
    equipment.push({ equipName: ref(''), equipNum: ref(''), availability: ref() })
}

// 删除项目
const removeEquipment = (item) => {
    const index = equipment.indexOf(item)
    if (index !== -1) {
        equipment.splice(index, 1)
    }
}


const equipmentName = ref([])  // 存放自动补全的设备名称

// 选择或根据输入提示设备名称
const querySearchEquipName = (queryString, cb) => {
    const results = queryString
        ? equipmentName.value.filter(createFilter(queryString))
        : equipmentName.value
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
const querySearchEquipNum = (queryString, cb) => {
    // 清除上一次选择的遗留选项
    templist.value = []
    // 获取设备对应编号列表
    equipmentName.value.forEach(obj => {
        if (obj.value === focusItem.value) {
            templist.value = obj.num
        }
    })
    // 提供列表
    const results = queryString
        ? templist.value.filter(createFilter(queryString))
        : templist.value
    // call callback function to return suggestions
    cb(results)
}


const loadEquipmentName = () => {
    return [
        { value: '生物安全柜', num: [{ value: "PD022-D" }, { value: "PD029-D" }] },
        { value: '超净工作台', num: [{ value: "PD023-D" }, { value: "PD030-D" }] },
        { value: '细胞计数仪', num: [{ value: "QC016-A" }] },
        { value: '二氧化碳培养箱', num: [{ value: "PD022-A" }, { value: "PD022-B" }, { value: "PD022-C" }, { value: "PD022-D" }] },
        { value: '倒置显微镜', num: [{ value: "PD027-C" }, { value: "PD027-D" }] },
        { value: '电动移液器', num: [{ value: "245423" }, { value: "245418" }] },
        { value: '高速离心机', num: [{ value: "PD025-A" }] },
        { value: '恒温水浴锅', num: [{ value: "RD003-A" }] },
        { value: '液氮罐', num: [{ value: "RD020-A" }] },
        { value: '-80℃冰箱', num: [{ value: "RD021-A" }] },
    ]
}

onMounted(() => {
    equipmentName.value = loadEquipmentName()
})
</script>

<template>
    <el-form class="notarise" :model="equipment">
        <el-row class="titleBox" :span="24">
            <el-col class="titleName" :span="7">
                <el-text class="equipName">设备名称</el-text>
            </el-col>
            <el-col class="titleName" :span="7">
                <el-text class="equipNum">编号</el-text>
            </el-col>
            <el-col class="titleName" :span="7">
                <el-text class="availability">是否符合要求</el-text>
            </el-col>
        </el-row>
        <el-row class="writeBox">
            <el-col :span="24">
                <el-form-item class="notariseItem" v-for="(item, index) in equipment" :key="index">
                    <el-col class="infoInput" :span="7">
                        <el-autocomplete :fetch-suggestions="querySearchEquipName" clearable placeholder="请输入设备名称"
                            v-model="item.equipName">
                            <!-- 设备名称 -->
                        </el-autocomplete>
                    </el-col>
                    <el-col class="infoInput" :span="7">
                        <el-autocomplete :fetch-suggestions="querySearchEquipNum" clearable placeholder="请输入设备编号"
                            v-model="item.equipNum" @focus="focusNum(equipment[index].equipName)">
                            <!-- 设备编号 -->
                        </el-autocomplete>
                    </el-col>
                    <el-col class="infoInput" :span="7">
                        <el-radio-group v-model="item.availability">
                            <el-radio :label="1">是</el-radio>
                            <el-radio :label="0">否</el-radio>
                        </el-radio-group>
                    </el-col>
                    <el-col class="infoInput" :span="3">
                        <el-button type="danger" round @click="removeEquipment(item)">删除</el-button>
                    </el-col>
                </el-form-item>
            </el-col>
            <el-col :span="3">
                <el-button type="primary" @click="addEquipment">+</el-button>
            </el-col>

        </el-row>
        {{ equipment }}
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