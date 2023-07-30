<script setup>
import { ref, reactive } from 'vue';

const cellCounted = reactive([
    { concentration: ref(2), indexes: ref(5), motilityRate: ref(), CakingRate: ref(0), volume: ref(40), totalCells: ref() },
])

// 自动计算细胞数量
const autoCount = (item) => {
    item.totalCells = item.concentration * (10 ** item.indexes) * item.volume
    // console.log(item.concentration)
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
                        <el-input-number v-model="item.indexes" clearable placeholder="指数" :step="1" @change="autoCount(cellCounted[index])"></el-input-number>
                    </el-col>
                    <el-col class="infoInput">
                        <el-tag>细胞活率(%)</el-tag>
                        <el-input-number v-model="item.motilityRate" clearable placeholder="细胞活率" :precision="1" :step="0.1"
                            :max="100" :min="0"></el-input-number>
                    </el-col>

                    <el-col class="infoInput">
                        <el-tag>结团率(%)</el-tag>
                        <el-input-number v-model="item.CakingRate" clearable placeholder="结团率" :precision="1" :step="0.1"
                            :max="100" :min="0"></el-input-number>
                    </el-col>

                    <el-col class="infoInput">
                        <el-tag>体积(mL)</el-tag>
                        <el-input-number v-model="item.volume" clearable placeholder="体积" :precision="1" :step="1"
                            :min="0" @change="autoCount(cellCounted[index])"></el-input-number>
                    </el-col>
                </el-form-item>
                {{ cellCounted }}
            </el-form>
        </el-col>
        <el-col class="countShow" :span="12">
            <el-table :data="cellCounted">
                <el-table-column prop="concentration" label="细胞浓度(cells/mL)"></el-table-column>
                <el-table-column prop="motilityRate" label="细胞活率(%)"></el-table-column>
                <el-table-column prop="CakingRate" label="细胞结团率(%)"></el-table-column>
                <el-table-column prop="volume" label="体积(mL)"></el-table-column>
                <el-table-column prop="totalCells" label="总数(cells)"></el-table-column>
            </el-table>
        </el-col>
    </el-row>
</template>