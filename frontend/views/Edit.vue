<template>
  <div class="page">
    <!-- page-title -->
    <h1 class="page-title">Edit</h1>

    <Editor
      id="editor-id"
      name="editor-name"
      v-model="content"
      :uploadImage="() => {}"
      :deleteImage="() => {}"
      :max-upload-size="maxUploadSize"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Editor from '@/components/editor/index.vue'

const content = ref('')
const maxUploadSize = ref(5 * 1024 * 1024)

// fetch course on mount
</script>

<style></style>
