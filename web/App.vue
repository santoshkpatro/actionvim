<script setup>
import { RouterView, RouterLink } from "vue-router";
</script>

<template>
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
</template>

<style scoped></style>
