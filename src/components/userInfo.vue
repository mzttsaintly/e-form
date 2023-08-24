<script setup>
import { useUserInfoStore, useLoginStore } from '../stores/counter';
import { onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'
const router = useRouter()
import baseUrl from '../assets/apilink.json';
// 保存用户信息
const userInfo = useUserInfoStore().userInfo
const tokenStore = useLoginStore()
// 生成的请求头
const gotHeaders = tokenStore.get_headers()
// 获取用户信息
const get_userInfo_url = baseUrl['baseUrl'] + 'get_userInfo'

const get_userInfo = () => {
    axios.post(get_userInfo_url, {}, gotHeaders).then(
        (response) => {
            console.log(response.data)
            userInfo.user_name = response.data.user_name;
            userInfo.user_authority = response.data.authority;
        }
    )
}

// 退出登录
const logout = () => {
    tokenStore.clearToken()
    router.push({ path: '/login' })
}

onMounted(() => {
    get_userInfo()
})
</script>

<template>
    <nut-cell>
        <el-input v-model="userInfo.user_name" disabled>
            <template #prepend>用户名：</template>
        </el-input>

        <el-input v-model="userInfo.user_authority" disabled>
            <template #prepend>权限等级：</template>
        </el-input>

        <nut-button type="primary" @click="logout">退出登录</nut-button>
    </nut-cell>
</template>