<script setup>
import { onMounted } from "vue";
const emit = defineEmits(["currentPage"]);

onMounted(() => {
  emit("currentPage", "views");
});
</script>

<template>
  <div>Views Page</div>
</template>
