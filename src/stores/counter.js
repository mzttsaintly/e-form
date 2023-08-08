import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

// export const useCounterStore = defineStore('counter', () => {
//   const count = ref(0)
//   const doubleCount = computed(() => count.value * 2)
//   function increment() {
//     count.value++
//   }

//   return { count, doubleCount, increment }
// })

export const useEquipmentStore = defineStore('equipment', () => {
  const equipment = reactive([
    { equipName: ref(''), equipNum: ref(''), place: ref(''), availability: ref(1) }
  ])
  return { equipment }
})

export const useMaterialStore = defineStore('material', () => {
  const materials = reactive([
    { material: ref(''), quantity: ref(''), lot: ref(''), POV: ref('') }
  ])

  return { materials }
})

export const useCellCountindStore = defineStore('cell', () => {
  const cellCounted = reactive([
    { concentration: ref(2), indexes: ref(5), combinationCounted: ref(''), motilityRate: ref(100), CakingRate: ref(0), volume: ref(40), totalCells: ref() },
])

  return { cellCounted }
})

export const useHeightStore = defineStore('height', () => {
  const scrollbarHeight = ref('80vh')
  return { scrollbarHeight }
})

export const useInoculumStore = defineStore('inoculum', () => {
  const inoculumSize = reactive({
    T150: ref(0),
    fivelayer: ref(1),
    tenlayer: ref(0),
    inoculumDensity: ref()
  })
  return { inoculumSize }
})