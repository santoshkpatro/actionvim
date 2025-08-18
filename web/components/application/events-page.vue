<script setup>
import { eventsListAPI, eventsSchemaAPI } from "@/api";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { Menu } from "lucide-vue-next";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(relativeTime);

const emit = defineEmits(["currentPage"]);

import EventProperties from "@/components/application/event-properties.vue";

const columns = [
  {
    key: "name",
    title: "Event",
    dataIndex: "name",
  },
  {
    key: "capturedAt",
    title: "Time",
  },
  {
    key: "source",
    title: "Source",
    dataIndex: "source",
  },
  {
    key: "action",
    width: 75,
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
  <a-table
    :columns="columns"
    :data-source="events"
    size="small"
    :pagination="false"
  >
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'capturedAt'">
        {{ dayjs(record.capturedAt).fromNow() }}
      </template>
      <template v-else-if="column.key === 'action'">
        <Menu class="w-4 h-4"></Menu>
      </template>
    </template>
    <template #expandedRowRender="{ record }">
      <event-properties :properties="JSON.parse(record.properties)" />
    </template>
  </a-table>
</template>
