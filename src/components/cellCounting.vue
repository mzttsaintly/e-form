<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useCellCountindStore, useHeightStore, useInoculumStore } from '../stores/counter';
// 表单数据
const cellCounted = useCellCountindStore().cellCounted
// const cellCounted = reactive([
//     { concentration: ref(2), indexes: ref(5), combinationCounted: ref(''), motilityRate: ref(100), CakingRate: ref(0), volume: ref(40), totalCells: ref(), COV: ref() },
// ])

// 获取当前总细胞数
const totalCellCount = ref()

// 计算能接种几个培养瓶
// 五层
const fiveLayer = computed(() => {
    return Math.ceil(totalCellCount.value / 8750000)
})
// 十层
const tenLayer = computed(() => {
    return Math.ceil(totalCellCount.value / 63200000)
})
// T150
const T150 = computed(() => {
    return Math.ceil(totalCellCount.value / 1500000)
})

// 自动计算细胞数量
const autoCount = (item) => {
    item.combinationCounted = (item.concentration * (10 ** item.indexes)).toExponential(2)
    item.totalCells = (item.concentration * (10 ** item.indexes) * item.volume).toExponential(2)
    // console.log(item.concentration)
}

// 新增计数结果
const addCounted = () => {
    cellCounted.push({ concentration: ref(2), indexes: ref(5), combinationCounted: ref(''), motilityRate: ref(100), CakingRate: ref(0), volume: ref(40), totalCells: ref() })
    autoCount(cellCounted[cellCounted.length - 1])
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
    const sums = []
    columns.forEach((column, index) => {
        if (index === 0) {
            sums[index] = '平均'
            return
        }
        const values = data.map((item) => Number(item[column.property]))
        let sum = 0;
        if (index === 1) {
            values.forEach(item => {
                sum += item;
            })
            sums[index] = (sum / values.length).toExponential(2);
        } else if (index === 5) {
            values.forEach(item => {
                sum += item;
            })
            totalCellCount.value = sum / values.length;
            sums[index] = (sum / values.length).toExponential(2);
        } else {
            values.forEach(item => {
                sum += item;
            })
            sums[index] = (sum / values.length);
        }
        if (index === 6) {
            sums[index] = 0
        }
    })
    autoCOV()
    return sums
}

// 计算每个数据的变异系数
const autoCOV = () => {
    if (totalCellCount.value != NaN) {
        cellCounted.forEach((item) => {
            let tempCOV = ((item.concentration * (10 ** item.indexes) * item.volume) - totalCellCount.value) / totalCellCount.value
            item.COV = (tempCOV * 100).toFixed(2)
        })
    }
}

// 种瓶数量统计以及平均密度计算
const inoculumSize = useInoculumStore().inoculumSize
// const inoculumSize = reactive({
//     T150: ref(),
//     fivelayer: ref(),
//     tenlayer: ref(),
//     inoculumDensity: ref()
//   })

// 自动计算平均密度
const inoculumDensity = computed(() => {
    return totalCellCount.value / (inoculumSize.fivelayer * 875 + inoculumSize.tenlayer * 6230 + inoculumSize.T150 * 150)
})

onMounted(() => {
    autoCount(cellCounted[0])
})
</script>

<template>
    <el-scrollbar :height="useHeightStore().scrollbarHeight">
        <!-- <el-col class="countInput"> -->
        <nut-divider>在此输入计数结果</nut-divider>
        <el-scrollbar :height="'500px'">
            <el-form class="cellCouted" :model="cellCounted" label-position="top">
                <el-form-item v-for="(item, index) in cellCounted" :key="index">
                    <nut-cell>
                        <el-tag type="info">{{ index + 1 }}</el-tag>
                        <el-space wrap direction="vertical">
                            <el-card class="countedCard">
                                <el-tag disable-transitions="true">细胞浓度(cells/mL)</el-tag>
                                <el-input-number v-model="item.concentration" clearable placeholder="细胞浓度" :precision="2"
                                    :step="0.1" :max="10" :min="0" @change="autoCount(cellCounted[index])"
                                    label="细胞浓度(cells/mL)"></el-input-number>
                                <el-text size="large">E</el-text>
                                <el-input-number v-model="item.indexes" clearable placeholder="指数" :step="1"
                                    @change="autoCount(cellCounted[index])"></el-input-number>
                            </el-card>
                            <el-card class="countedCard">
                                <el-tag disable-transitions="true">细胞活率(%)</el-tag>
                                <el-input-number v-model="item.motilityRate" clearable placeholder="细胞活率" :precision="1"
                                    :step="0.1" :max="100" :min="0"></el-input-number>
                            </el-card>
                            <el-card class="countedCard">
                                <el-tag disable-transitions="true">结团率(%)</el-tag>
                                <el-input-number v-model="item.CakingRate" clearable placeholder="结团率" :precision="1"
                                    :step="1" :max="100" :min="0"></el-input-number>
                            </el-card>
                            <el-card class="countedCard">
                                <el-tag disable-transitions="true">体积(mL)</el-tag>
                                <el-input-number v-model="item.volume" clearable placeholder="体积" :precision="1" :step="1"
                                    :min="0" @change="autoCount(cellCounted[index])"></el-input-number>
                            </el-card>
                        </el-space>
                        <el-button type="danger" round @click="removeCounted(item)">删除</el-button>
                    </nut-cell>


                </el-form-item>
                <!-- {{ cellCounted }} -->
                <el-button class="addCounted" type="primary" @click="addCounted">+</el-button>
            </el-form>
        </el-scrollbar>

        <nut-divider>以下为统计结果</nut-divider>
        <!-- </el-col> -->
        <el-col class="countShow">
            <el-table class="cellCounted" :data="cellCounted" show-summary :summary-method="getSverageValue">
                <el-table-column type="index" :index="indexMethod" />
                <el-table-column prop="combinationCounted" label="细胞浓度(cells/mL)"></el-table-column>
                <el-table-column prop="motilityRate" label="细胞活率(%)"></el-table-column>
                <el-table-column prop="CakingRate" label="细胞结团率(%)"></el-table-column>
                <el-table-column prop="volume" label="体积(mL)"></el-table-column>
                <el-table-column prop="totalCells" label="总数(cells)"></el-table-column>
                <el-table-column prop="COV" label="变异系数(%)"></el-table-column>
            </el-table>
            <el-divider />
            <el-card class="howMuchLayer">
                <template #header>
                    <div class="card-header">
                        <span>可以种多少瓶培养瓶(向上取整)</span>
                    </div>
                </template>
                <el-row>
                    <!-- <el-tag>五层培养瓶：{{ fiveLayer }}个</el-tag> -->
                    <el-col :span="6">
                        <el-statistic title="五层培养瓶：" :value="fiveLayer" suffix="个"></el-statistic>
                    </el-col>

                    <el-col :span="6">
                        <el-statistic title="十层工厂：" :value="tenLayer" suffix="个"></el-statistic>
                    </el-col>
                    <!-- <el-tag class="ml-2" type="success">十层工厂：{{ tenLayer }}个</el-tag> -->

                    <el-col :span="6">
                        <el-statistic title="T150：" :value="T150" suffix="个"></el-statistic>
                    </el-col>
                    <!-- <el-tag class="ml-2" type="warning">T150：{{ T150 }}个</el-tag> -->
                </el-row>
            </el-card>
            <el-divider />
            <el-card>
                <template #header>
                    <div class="card-header">
                        <span>平均细胞密度：</span>
                    </div>
                </template>
                <el-form :model="inoculumSize" label-position="Right" label-width="auto">
                    <el-form-item label="五层培养瓶：(875平方厘米)">
                        <el-input-number v-model="inoculumSize.fivelayer" :step="1" step-strictly min="0"></el-input-number>
                    </el-form-item>
                    <el-form-item label="十层细胞工厂：(6230平方厘米)">
                        <el-input-number v-model="inoculumSize.tenlayer" :step="1" step-strictly min="0"></el-input-number>
                    </el-form-item>
                    <el-form-item label="T150培养瓶:(150平方厘米)">
                        <el-input-number v-model="inoculumSize.T150" :step="1" step-strictly min="0"></el-input-number>
                    </el-form-item>
                </el-form>
                <!-- <el-tag>平均密度：{{ inoculumDensity }} 个/平方厘米</el-tag> -->
                <el-statistic title="平均密度：" :value="inoculumDensity" suffix="个/平方厘米"></el-statistic>
            </el-card>
        </el-col>

    </el-scrollbar>
</template>

<style>
.countedCard {
    width: 70vw;
}
</style>