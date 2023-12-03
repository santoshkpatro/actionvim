<script setup>
import { onMounted } from 'vue'
import axios from 'axios'
import { http } from '@/api/index'

onMounted(async () => {
  await http.get('/api/user/profile')
})
</script>

<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<style>

</style>
