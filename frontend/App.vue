<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { rawHttp, http } from '@/api'
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'

// import Spinner from '@/components/base/Spinner.vue'

const userStore = useUserStore()
const isLoading = ref(false)

onMounted(async () => {
  const refresh = localStorage.getItem("token")
  if (!refresh) return

  try {
    isLoading.value = true
    const { data } = await rawHttp.post("/api/user/token/", { token: refresh })
    userStore.setUser(data)
    http.defaults.headers.common['Authorization'] = `Bearer ${data.tokens.access}`
  } catch (error) {
    localStorage.removeItem("token")
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div v-if="isLoading" class="center-container">
    <Loader />
  </div>
  <div v-else>
    <RouterView />
  </div>
</template>

<style>
.center-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 90vh;
}
</style>
