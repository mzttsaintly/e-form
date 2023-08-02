<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import baseUrl from '../assets/apilink.json'

const addEquipment = reactive([{
    equipName: ref(''),
    equipNum: ref(''),
    place: ref('')
}])

const addM = () => {
    addEquipment.push({
        equipName: ref(''),
        equipNum: ref(''),
        place: ref('')
    })
}

// 提交数据
const addEquipmentUrl = baseUrl['baseUrl'] + 'add_Equipments'

const pushMaterial = () => {
    axios.post(addEquipmentUrl, addEquipment).then(
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
</script>

<template>
    <el-form :model="addMaterial">
        <el-form-item v-for="(item, index) in addEquipment" :key="index">
            <el-tag>{{ index+1 }}</el-tag>
            <el-input v-model="item.equipName"><template #prepend>设备名称</template></el-input>
            <el-input v-model="item.equipNum"><template #prepend>设备编号</template></el-input>
            <el-input v-model="item.place"><template #prepend>存放地点</template></el-input>
        </el-form-item>
        <el-button type="primary" @click="addM">+</el-button>
    </el-form>
    <el-button @click="pushMaterial" type="info">提交</el-button>
</template>