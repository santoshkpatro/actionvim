<script setup>
import { useRouter } from "vue-router";
import { Home, Mail, Github } from "lucide-vue-next";

const router = useRouter();

const supportEmail = "support@actionvim.com";
const githubUrl = "https://github.com/actionvim/issues";
</script>

<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-white text-gray-900 px-6"
  >
    <!-- Code -->
    <p class="text-sm font-semibold text-indigo-600">404</p>

    <!-- Heading -->
    <h1 class="mt-2 text-3xl font-bold tracking-tight">Page not found</h1>
    <p class="mt-2 text-sm text-gray-600">
      Sorry, the page you are looking for doesn’t exist. If the problem
      persists, please contact support, check GitHub issues, or reach out to
      your system administrator.
    </p>

    <!-- Actions -->
    <div class="mt-6 flex gap-3">
      <button
        @click="router.push('/')"
        class="inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium text-white shadow-sm"
      >
        <Home class="h-4 w-4" />
        Go Home
      </button>

      <a
        :href="`mailto:${supportEmail}`"
        class="inline-flex items-center gap-2 rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 no-underline"
      >
        <Mail class="h-4 w-4" />
        Contact Support
      </a>

      <a
        :href="githubUrl"
        target="_blank"
        rel="noopener"
        class="inline-flex items-center gap-2 rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 no-underline"
      >
        <Github class="h-4 w-4" />
        GitHub Issues
      </a>
    </div>
  </div>
</template>
