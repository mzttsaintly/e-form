import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'
import { rateEmits } from 'element-plus'

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
    { concentration: ref(2), indexes: ref(5), combinationCounted: ref(''), motilityRate: ref(100), CakingRate: ref(0), volume: ref(40), totalCells: ref(), COV: ref() },
])

  return { cellCounted }
})

export const useHeightStore = defineStore('height', () => {
  const scrollbarHeight = ref('85vh')
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

// 获取报告的表单
export const useReportStore = defineStore('report', () => {
  const reportList = reactive([])
  const reportTable = reactive({
    uploadMaterial: reactive([]),
    uploadEquipment: reactive([]),
    uploadCells: reactive([])
  })
  return { reportList, reportTable }
})

// 保存登录信息
export const useLoginStore = defineStore('login', () => {
  const userToken = ref('')
  function changeToken(newToken) {
    userToken.value = newToken
  }
  function clearToken() {
    userToken.value = ''
  }
  function get_headers() {
    let temp_headers = {
      headers:{
        'authorization': userToken.value
    }
    }
    return temp_headers
  }
  function notarizeLogin() {
    return userToken.value !== ''
  }
  return { userToken, changeToken, clearToken, get_headers, notarizeLogin }
})

// 侧边导航栏是否打开
export const useSideBarStore = defineStore('sidebar', () => {
  const sideBarState = reactive({
    show: false,
    width: '50%',
    height: '100%'
  })
  function handleClick() {
    sideBarState.show = true
  }
  return { sideBarState, handleClick }
})

// 保存用户登录信息
export const useUserInfoStore = defineStore('userInfo', () => {
  const userInfo = reactive({
    user_name: ref(''),
    user_authority: ref(0)
  })
  return { userInfo }
})