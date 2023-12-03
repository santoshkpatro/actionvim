<script setup>
import { reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { http, rawHttp } from '@/api'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()

const userStore = useUserStore()
const formState = reactive({
  username: '',
  password: '',
  remember: true,
})
const onFinish = async (values) => {
  console.log('Success:', values)

  const { data } = await rawHttp.post('/api/user/sign_in/', values)
  localStorage.setItem("token", data.user.tokens.refresh)

  http.defaults.headers.common['Authorization'] = `Bearer ${data.user.tokens.access}`
  userStore.setUser(data.user)

  router.push({ name: 'home' })
}
const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo)
}
</script>

<template>
  <div class="center-container">
    <a-form
      :model="formState"
      name="basic"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 16 }"
      autocomplete="off"
      @finish="onFinish"
      @finishFailed="onFinishFailed"
    >
      <a-form-item
        label="Username"
        name="username"
        :rules="[{ required: true, message: 'Please input your username!' }]"
      >
        <a-input v-model:value="formState.username" />
      </a-form-item>

      <a-form-item
        label="Password"
        name="password"
        :rules="[{ required: true, message: 'Please input your password!' }]"
      >
        <a-input-password v-model:value="formState.password" />
      </a-form-item>

      <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
        <a-button type="primary" html-type="submit">Submit</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<style>

</style>
