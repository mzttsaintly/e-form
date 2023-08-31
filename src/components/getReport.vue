<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import baseUrl from '../assets/apilink.json';

import { useHeightStore, useLoginStore } from '../stores/counter';

// 从服务器获得token
const tokenStore = useLoginStore()
// 生成的请求头
const gotHeaders = tokenStore.get_headers()

// 报告列表的代理对象
const reportListRef = ref()

// 关闭报告单详情时取消表格选择
const setCurrentNone = (row) => {
    reportListRef.value.setCurrentRow(row)
}

// 从服务器获取的报告列表
const reportList = reactive([])

const getReportList = () => {
    axios.post(baseUrl['baseUrl'] + 'return_report_list',{}, gotHeaders).then(
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
const reportTable = reactive({
    uploadMaterial: reactive([]),
    uploadEquipment: reactive([]),
    uploadCells: reactive([])
})

const getReportTable = (filename) => {
    let getReportValue = { filename: filename }
    axios.post(baseUrl['baseUrl'] + 'return_report_json', getReportValue, gotHeaders).then(
        (response) => {
            // console.log(response.data)
            let res = JSON.parse(response.data)
            reportTable.uploadMaterial = res.uploadMaterial
            reportTable.uploadEquipment = res.uploadEquipment
            reportTable.uploadCells = res.uploadCells
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
    if (tokenStore.notarizeLogin()) {
        getReportList()
    } else {
        ElMessageBox.alert('请先登录', '未登录', )
    }
    
})

// 选中列表项目时
const handleReport = (val) => {
    console.log(val)
    if (val != null) {
        getReportTable(val.name)
    }

}

// 报告详情页是否显示
const reportTableVisible = ref(false)
// const reportTitle = ref('')

</script>

<template>
    <el-scrollbar :height="useHeightStore().scrollbarHeight">
        <!-- {{ reportList }} -->
        <el-table :data="reportList" highlight-current-row @current-change="handleReport" ref="reportListRef">
            <el-table-column type="index" label="序号" width="100" />
            <el-table-column prop="name" label="报告名称"></el-table-column>
        </el-table>
        <!-- {{ reportTable }} -->
    </el-scrollbar>

    <!-- 报告详情页 -->
    <el-dialog id="printBox" v-model="reportTableVisible" @close="setCurrentNone()" width="90vw">
        <nut-divider>物料详情</nut-divider>
        <nut-cell>
            <el-table :data="reportTable.uploadMaterial">
                <el-table-column type="index" label="序号" width="100"></el-table-column>
                <el-table-column prop="material" label="物料名称"></el-table-column>
                <el-table-column prop="lot" label="物料批号"></el-table-column>
                <el-table-column prop="POV" label="有效期/复验期"></el-table-column>
                <el-table-column prop="quantity" label="数量"></el-table-column>
            </el-table>
        </nut-cell>

        <nut-divider>设备详情</nut-divider>
        <nut-cell>
            <el-table :data="reportTable.uploadEquipment">
                <el-table-column type="index" label="序号" width="100"></el-table-column>
                <el-table-column prop="equipName" label="设备名称"></el-table-column>
                <el-table-column prop="equipNum" label="设备编号"></el-table-column>
                <el-table-column prop="place" label="登记位置"></el-table-column>
                <el-table-column prop="availability" label="是否可用"></el-table-column>
            </el-table>
        </nut-cell>

        <nut-divider>细胞计数详情</nut-divider>
        <nut-cell>
            <el-table :data="reportTable.uploadCells">
                <el-table-column type="index" label="序号" width="100"></el-table-column>
                <el-table-column prop="combinationCounted" label="细胞浓度"></el-table-column>
                <el-table-column prop="motilityRate" label="细胞活率(%)"></el-table-column>
                <el-table-column prop="CakingRate" label="结团率(%)"></el-table-column>
                <el-table-column prop="volume" label="体积(mL)"></el-table-column>
                <el-table-column prop="totalCells" label="细胞总数"></el-table-column>
                <el-table-column prop="COV" label="变异系数(%)"></el-table-column>
            </el-table>
        </nut-cell>

        <template #footer>
            <span class="dialog-footer">
                <!-- <el-button @click="reportTableVisible = false">取消</el-button> -->
                <el-button v-print="'#printBox'">打印</el-button>
                <el-button type="primary" @click="reportTableVisible = false">
                    确认
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>