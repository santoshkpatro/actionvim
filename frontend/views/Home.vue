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
</script>

<template>
  <main>
    <h1>Projects</h1>

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
