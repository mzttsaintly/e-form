<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import baseUrl from '../assets/apilink.json';

import { useReportStore, useHeightStore } from '../stores/counter';

// 从服务器获取的报告列表
const reportList = useReportStore().reportList

const getReportList = () => {
    axios.post(baseUrl['baseUrl'] + 'return_report_list').then(
        (response) => {
            let res = response.data
            console.log(res)
            res.forEach((item) => {
                reportList.push({ name: item })
            })
        }
    ).catch((err) => {
        ElMessageBox.alert(err, '服务器错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}


// 从服务器获取的报告内容
const reportTable = useReportStore().reportTable

const getReportTable = (filename) => {
    let getReportValue = {filename: filename}
    axios.post(baseUrl['baseUrl'] + 'return_report_json', getReportValue).then(
        (response) => {
            // console.log(response.data)
            let res = JSON.parse(response.data)

            reportTable.uploadMaterial = res.uploadMaterial
            reportTable.uploadEquipment = res.uploadEquipment
            reportTable.uploadCells.value = res.uploadCells
            reportTableVisible.value = true
            // reportTable
        }
    ).catch((err) => {
        ElMessageBox.alert(err, '服务器错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}

// 组件加载时的钩子函数，获取报告列表
onMounted(() => {
    getReportList()
})

// 选中列表项目时
const handleReport = (val) => {
    console.log(val)
    getReportTable(val.name)
}

// 报告详情页是否显示
const reportTableVisible = ref(false)
// const reportTitle = ref('')
</script>

<template>
    <el-scrollbar :height="useHeightStore().scrollbarHeight">
        {{ reportList }}
        <el-table :data="reportList" highlight-current-row @current-change="handleReport">
            <el-table-column type="index" label="序号" width="100" />
            <el-table-column prop="name" label="报告名称"></el-table-column>
        </el-table>
        {{ reportTable }}
    </el-scrollbar>

    <!-- 报告详情页 -->
    <el-dialog v-model="reportTableVisible">
        <el-table :data="reportTable.uploadMaterial">
            <el-table-column  type="index" label="序号" width="100" ></el-table-column>
            <el-table-column prop="material" label="物料名称"></el-table-column>
            <el-table-column prop="lot" label="物料批号"></el-table-column>
            <el-table-column prop="POV" label="有效期/复验期"></el-table-column>
            <el-table-column prop="quantity" label="数量"></el-table-column>
            
        </el-table>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="reportTableVisible = false">Cancel</el-button>
                <el-button type="primary" @click="reportTableVisible = false">
                    Confirm
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>