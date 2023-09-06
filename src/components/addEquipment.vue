<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import baseUrl from '../assets/apilink.json';
import { useLoginStore, useHeightStore } from '../stores/counter';

// 从服务器获得token
const tokenStore = useLoginStore()
// 生成的请求头
const gotHeaders = tokenStore.get_headers()

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
    axios.post(addEquipmentUrl, addEquipment, gotHeaders).then(
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

// 删除条目
const del_url = baseUrl['baseUrl'] + 'use_del_equipments'

// 删除前确认
const verifyDelEquipments = async (id) => {
    ElMessageBox.confirm('确定删除该条目？', '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(
        async () => {
            await delEquipments(id)
        }
    )
}

const delEquipments = async (id) => {
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

const getEquipmentUrl = baseUrl['baseUrl'] + 'queryEquipments'

// 临时存储从服务器获取的数据
const severData = reactive([])

// 从服务器获取数据
const getSeverData = async () => {
    await axios.post(getEquipmentUrl).then(
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

onMounted(async () => {
    await getSeverData()
})


// 需编辑的行所在的index
const editIndex = ref(-1)

// 设置将要编辑的行index
const handleEdit = async (row) => {
    if (editIndex.value !== row.id) {
        editIndex.value = row.id
    } else {
        let tempInfo = {
            equipments_id: row.id,
            equipName: row.equipName,
            equipNum: row.equipNum,
            place: row.place
        }
        ElMessageBox.confirm(`设备名称:${tempInfo.equipName},设备编号:${tempInfo.equipNum},登记地点:${tempInfo.place}`, '确认修改', {
            confirmButtonText: '是',
            cancelButtonText: '否',
            type: 'warning',
        }).then(async () => {
            console.log(tempInfo)
            await modifyEquipments(tempInfo)
            await getSeverData()
        }).catch(async () => {
            await getSeverData()
        })
        editIndex.value = -1

    }

}

// 修改条目
const modifyUrl = baseUrl['baseUrl'] + 'modify_equipments'

const modifyEquipments = async (modifyInfo) => {
    await axios.post(modifyUrl, modifyInfo, gotHeaders).then((response) => {
        ElMessage(response.data)
    }).catch((err) => {
        console.log(err)
        ElMessage(err)
    })
}
</script>

<template>
    <nut-tabs>
        <nut-tab-pane title="设备信息查询">
            <el-scrollbar :height="useHeightStore().scrollbarHeight">
                <el-table :data="severData">
                    <el-table-column prop="id" label="ID" sortable>

                    </el-table-column>

                    <el-table-column prop="equipName" label="设备名称" sortable>
                        <template v-slot="editRow">
                            <span v-show="editRow.row.id !== editIndex">{{ editRow.row.equipName }}</span>
                            <el-input v-show="editRow.row.id === editIndex" v-model="editRow.row.equipName"></el-input>
                        </template>
                    </el-table-column>

                    <el-table-column prop="equipNum" label="设备编号" sortable>
                        <template v-slot="editRow">
                            <span v-show="editRow.row.id !== editIndex">{{ editRow.row.equipNum }}</span>
                            <el-input v-show="editRow.row.id === editIndex" v-model="editRow.row.equipNum"></el-input>
                        </template>
                    </el-table-column>

                    <el-table-column prop="place" label="登记地点" sortable>
                        <template v-slot="editRow">
                            <span v-show="editRow.row.id !== editIndex">{{ editRow.row.place }}</span>
                            <el-input v-show="editRow.row.id === editIndex" v-model="editRow.row.place"></el-input>
                        </template>
                    </el-table-column>

                    <el-table-column label="操作">
                        <template v-slot="editRow">
                            <el-button @click="handleEdit(editRow.row)">
                                <el-icon>
                                    <EditPen v-show="editRow.row.id !== editIndex" />
                                    <Select v-show="editRow.row.id === editIndex"></Select>
                                </el-icon>
                            </el-button>

                            <el-tooltip content="删除条目">
                                <el-button type="danger" @click="verifyDelEquipments(editRow.row.id)"><el-icon>
                                        <CloseBold />
                                    </el-icon></el-button>
                            </el-tooltip>
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </nut-tab-pane>

        <nut-tab-pane title="设备信息录入">
            <el-form :model="addMaterial">
                <el-form-item v-for="(item, index) in addEquipment" :key="index">
                    <el-tag>{{ index + 1 }}</el-tag>
                    <el-input v-model="item.equipName"><template #prepend>设备名称</template></el-input>
                    <el-input v-model="item.equipNum"><template #prepend>设备编号</template></el-input>
                    <el-input v-model="item.place"><template #prepend>存放地点</template></el-input>
                </el-form-item>
                <el-button type="primary" @click="addM">+</el-button>
            </el-form>
            <el-button @click="pushMaterial" type="info">提交</el-button>
        </nut-tab-pane>
    </nut-tabs>
</template>