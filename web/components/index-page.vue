<script setup>
import { applicationsListAPI } from "@/api";
import { onMounted } from "vue";
import { useStore } from "@/store";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();

const loadApplications = async () => {
  const applications = await applicationsListAPI();
  if (!applications.length > 0) {
    router.push({ name: "application-create" });
    return;
  }

  //   store.setApplications(applications);
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
