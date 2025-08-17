<script setup>
import { applicationsMineAPI } from "@/api";
import { onMounted } from "vue";
import { useStore } from "@/store";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();

const loadApplications = async () => {
  const applications = await applicationsMineAPI();
  if (!applications.length > 0) {
    router.push({ name: "application-create" });
    return;
  }

  router.push({
    name: "dashboard",
    params: { applicationId: applications[0].id },
  });
};

onMounted(() => {
  loadApplications();
});
</script>

<template>
  <div>Index Page</div>
</template>
