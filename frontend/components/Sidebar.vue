<template>
  <a-menu
    v-model:openKeys="openKeys"
    v-model:selectedKeys="selectedKeys"
    style="max-width: 200px; height: 100vh; position: inline-block"
    mode="inline"
    :theme="theme"
    :items="items"
  />
</template>

<script setup>
import { h, ref } from 'vue'
import { MailOutlined, CalendarOutlined } from '@ant-design/icons-vue'

const theme = ref('dark')
const selectedKeys = ref(['1'])
const openKeys = ref(['sub1'])
const items = ref([
  {
    key: '1',
    icon: () => h(MailOutlined),
    label: 'Formester',
    title: 'Formester',
  },
  {
    key: '2',
    icon: () => h(CalendarOutlined),
    label: 'Nexus',
    title: 'Nexus',
  },
  {
    key: '3',
    icon: () => h(CalendarOutlined),
    label: 'Eitoss',
    title: 'Eitoss',
  },
])
</script>

<style></style>
