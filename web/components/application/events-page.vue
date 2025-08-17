<script setup>
import { eventsListAPI, eventsSchemaAPI } from "@/api";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const emit = defineEmits(["currentPage"]);

import EventProperties from "@/components/application/event-properties.vue";

const columns = [
  {
    title: "Event",
    dataIndex: "name",
  },
  {
    title: "Ref ID",
    dataIndex: "id",
  },
  {
    title: "Captured at",
    dataIndex: "capturedAt",
  },
  {
    title: "Action",
  },
];

const route = useRoute();
const events = ref([]);
const schema = ref({
  eventNames: [],
});

const loadRecentEvents = async () => {
  const recentEvents = await eventsListAPI(route.params.applicationId);
  events.value = recentEvents.map((e) => {
    return {
      ...e,
      key: e.id,
    };
  });
};

const loadEventSchema = async () => {
  schema.value = await eventsSchemaAPI(route.params.applicationId);
};

onMounted(() => {
  emit("currentPage", "events");

  loadEventSchema();
  loadRecentEvents();
});
</script>

<template>
  <a-table :columns="columns" :data-source="events">
    <template #expandedRowRender="{ record }">
      <event-properties :properties="JSON.parse(record.properties)" />
    </template>
  </a-table>
</template>
