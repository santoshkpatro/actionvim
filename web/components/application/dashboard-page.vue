<script setup>
import { onMounted } from "vue";

const emit = defineEmits(["currentPage"]);

const loadDashboardData = () => {
  // Logic to load dashboard data
  console.log("Loading dashboard data...");
};

onMounted(() => {
  emit("currentPage", "dashboard");
  loadDashboardData();
});
</script>

<template>
  <div>Dashboard Page</div>
</template>
