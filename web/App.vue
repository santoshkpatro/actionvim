<script setup>
import { RouterView, RouterLink } from "vue-router";

const themeOverride = {
  token: {
    borderRadius: 4,
    fontFamily: "Inter, sans-serif",
    colorPrimary: "#1f4d8c",
  },
};
</script>

<template>
  <a-config-provider :theme="themeOverride">
    <router-view></router-view>
  </a-config-provider>
</template>

<style scoped></style>
