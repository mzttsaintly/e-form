<script setup>
import { ref, reactive } from 'vue';

const cellCounted = reactive([
    { concentration: ref(2), indexes: ref(5), combinationCounted: ref(''), motilityRate: ref(100), CakingRate: ref(0), volume: ref(40), totalCells: ref() },
])

// 组合细胞浓度
const combination = () => {

}


// 自动计算细胞数量
const autoCount = (item) => {
    item.combinationCounted = (item.concentration * (10 ** item.indexes)).toExponential(2)
    item.totalCells = (item.concentration * (10 ** item.indexes) * item.volume).toExponential(2)
    // console.log(item.concentration)
}

// 新增计数结果
const addCounted = () => {
    cellCounted.push({ concentration: ref(2), indexes: ref(5), combinationCounted: ref(''), motilityRate: ref(100), CakingRate: ref(0), volume: ref(40), totalCells: ref() })
}

// 删除计数结果
const removeCounted = (item) => {
    const index = cellCounted.indexOf(item)
    if (index !== -1) {
        cellCounted.splice(index, 1)
    }
}

// 自动求平均值
const getSverageValue = (param) => {
    const { columns, data } = param
    console.log(data)
    const sums = []
    columns.forEach((column, index) => {
        if (index === 0) {
            sums[index] = '平均'
            return
        }
        const values = data.map((item) => Number(item[column.property]))
        let sum = 0;
        if (index === 1 || index === 5) {
            values.forEach(item => {
            sum += item;
        })
        sums[index] = (sum / values.length).toExponential(2);
        } else {
            values.forEach(item => {
            sum += item;
        })
        sums[index] = (sum / values.length);
        }
    })
    return sums
}
</script>

<template>
    <el-row class="cellCounting">
        <el-col class="countInput" :span="12">
            <el-form :model="cellCounted" label-position="top">
                <el-form-item label="计数结果" v-for="(item, index) in cellCounted" :key="index">
                    <el-col class="infoInput">
                        <el-tag>细胞浓度(cells/mL)</el-tag>
                        <el-input-number v-model="item.concentration" clearable placeholder="细胞浓度" :precision="2"
                            :step="0.1" :max="10" :min="0" @change="autoCount(cellCounted[index])"></el-input-number>
                        E
                        <el-input-number v-model="item.indexes" clearable placeholder="指数" :step="1"
                            @change="autoCount(cellCounted[index])"></el-input-number>
                    </el-col>
                    <el-col class="infoInput">
                        <el-tag>细胞活率(%)</el-tag>
                        <el-input-number v-model="item.motilityRate" clearable placeholder="细胞活率" :precision="1" :step="0.1"
                            :max="100" :min="0"></el-input-number>
                    </el-col>

                    <el-col class="infoInput">
                        <el-tag>结团率(%)</el-tag>
                        <el-input-number v-model="item.CakingRate" clearable placeholder="结团率" :precision="1" :step="1"
                            :max="100" :min="0"></el-input-number>
                    </el-col>

                    <el-col class="infoInput">
                        <el-tag>体积(mL)</el-tag>
                        <el-input-number v-model="item.volume" clearable placeholder="体积" :precision="1" :step="1" :min="0"
                            @change="autoCount(cellCounted[index])"></el-input-number>
                    </el-col>
                    <el-col class="infoInput" :span="3">
                        <el-button type="danger" round @click="removeCounted(item)">删除</el-button>
                    </el-col>
                </el-form-item>
                {{ cellCounted }}
            </el-form>
            <el-button type="primary" @click="addCounted">+</el-button>
        </el-col>
        <el-col class="countShow" :span="12">
            <el-table :data="cellCounted" show-summary :summary-method="getSverageValue">
                <el-table-column type="index" :index="indexMethod" />
                <el-table-column prop="combinationCounted" label="细胞浓度(cells/mL)"></el-table-column>
                <el-table-column prop="motilityRate" label="细胞活率(%)"></el-table-column>
                <el-table-column prop="CakingRate" label="细胞结团率(%)"></el-table-column>
                <el-table-column prop="volume" label="体积(mL)"></el-table-column>
                <el-table-column prop="totalCells" label="总数(cells)"></el-table-column>
            </el-table>
        </el-col>
    </el-row>
</template>