<script setup>
import { useRouter, useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'
import { http } from '@/api'

// components
import Sidebar from '@/components/Sidebar.vue'
import Kanban from '@/components/Kanban.vue'

const router = useRouter()
const route = useRoute()

onMounted(async () => {
  try {
    await http.get(`/api/projects/${route.params.public_id}/`)
  } catch (e) {
    console.log(e)
  }
})

const lists = ref([
  { title: 'To Do', cards: ['Task 1', 'Task 2'] },
  { title: 'In Progress', cards: ['Task 3', 'Task 4'] },
  { title: 'Done', cards: ['Task 5', 'Task 6'] },
])
</script>

<template>
  <a-flex>
    <Sidebar />
    <Kanban />
  </a-flex>
</template>
