<script setup>
import { reactive, ref } from 'vue';
import { useLoginStore, useHeightStore } from '../stores/counter';
import { storeToRefs } from 'pinia';
import axios from 'axios';
import baseUrl from '../assets/apilink.json';

// 保存的token
const tokenStore = useLoginStore()
const loginToken = storeToRefs(tokenStore)
// 输入的登录数据
const userForm = reactive({
    user_name: ref(''),
    password: ref('')
})

// 表单对象代理
const userFormRef = ref()

// 密码框对象代理
const passwordInput = ref()

// 登录获取token
const login_url = baseUrl['baseUrl'] + 'login'

const login = () => {
    axios.post(login_url, userForm).then(
        (response) => {
            let res = response.data.access_token
            console.log(res)
            tokenStore.changeToken(res)
        }
    ).catch((err) => {
        ElMessageBox.alert(err.response.data, '发生错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}
</script>

<template>
    <nut-cell>
        <el-form ref="userFormRef">
            <el-form-item label="用户名：">
                <el-input v-model="userForm.user_name" clearable
                    @keyup.enter.native="() => passwordInput.focus()"></el-input>
            </el-form-item>
            <el-form-item label="密码：">
                <el-input ref="passwordInput" type="password" v-model="userForm.password" clearable
                    @keyup.enter.native="login"></el-input>
            </el-form-item>
            <nut-button type="default" @click="resetFields(userFormRef)">清空</nut-button>
            <nut-button type="success" @click="login">登录</nut-button>
            <nut-button type="default" @click="console.log(loginToken.userToken.value)">token</nut-button>
        </el-form>

    </nut-cell>
</template>