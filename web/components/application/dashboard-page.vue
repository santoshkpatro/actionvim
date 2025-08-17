<script setup>
import { onMounted } from "vue";

const emit = defineEmits(["currentPage"]);

onMounted(() => {
  emit("currentPage", "dashboard");
});
</script>

<template>
  <div>Dashboard Page</div>
</template>
