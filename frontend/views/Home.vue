<script setup>
import { RouterLink } from 'vue-router'
import { rawHttp, http } from '@/api'
import { onMounted, ref } from 'vue'

const projects = ref([])

onMounted(async () => {
  try {
    const { data } = await http.get('/api/projects/')
    projects.value = data
  } catch (error) {
    console.log(error)
  }
})

const handleLogout = async () => {
  try {
    await http.get("/api/user/logout/")
    localStorage.removeItem("user")
    window.location.reload()
  } catch (error) {
    console.log(error)    
  }
}
</script>

<template>
  <main>
    <h1>Projects</h1>
    <a-button type="dashed" @click="handleLogout">Logout</a-button>

    <RouterLink :to="{ name: 'project-detail', params: { public_id: project.public_id } }" v-for="project in projects" :key="project.id">
      <a-card :title="project.title" style="width: 300px">
      </a-card>
    </RouterLink>
  </main>
</template>

<style scoped>
a {
  text-decoration: none;
}
</style>
