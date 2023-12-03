<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { rawHttp, http } from '@/api'
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'

// import Spinner from '@/components/base/Spinner.vue'

const userStore = useUserStore()
const isLoading = ref(false)

onMounted(async () => {
  try {
    isLoading.value = true
    const { data } = await rawHttp.get("/api/user/profile/")
    userStore.setUser(data)
    // http.defaults.headers.common['Authorization'] = `Bearer ${data.tokens.access}`
    localStorage.setItem("user", JSON.stringify(data))
  } catch (error) {
    localStorage.removeItem("user")
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
