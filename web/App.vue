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
    <div class="app">
      <header>
        <h1>ActionVim</h1>
        <nav style="display: flex; gap: 10px">
          <router-link to="/">Home</router-link>
          <router-link to="/login">Login</router-link>
        </nav>
      </header>
    </div>
    <router-view></router-view>
  </a-config-provider>
</template>

<style scoped></style>
