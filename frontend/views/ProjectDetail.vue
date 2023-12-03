<script setup>
import { useRouter, useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'
import { http } from '@/api'

const router = useRouter()
const route = useRoute()

console.log(route.params.public_id)

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
    Project Detail View
    <div>
        <a-flex>
            <a-card title="Card title" style="width: 300px">
            </a-card>
        </a-flex>
    </div>
</template>