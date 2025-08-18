<script setup>
import { eventsListAPI, eventsSchemaAPI } from "@/api";
import { ref, onMounted, h, computed } from "vue";
import { useRoute } from "vue-router";
import { Menu } from "lucide-vue-next";
import { CalendarOutlined } from "@ant-design/icons-vue";
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

const loading = ref(false);
const route = useRoute();
const events = ref([]);
const schema = ref({
  eventNames: [],
});

const filters = ref({
  start: dayjs().startOf("day").toISOString(),
  end: dayjs().endOf("day").toISOString(),
});
const loadEvents = async () => {
  loading.value = true;
  const recentEvents = await eventsListAPI(
    route.params.applicationId,
    filters.value
  );
  events.value = recentEvents.map((e) => {
    return {
      ...e,
      key: e.id,
    };
  });
  loading.value = false;
};

const loadEventSchema = async () => {
  schema.value = await eventsSchemaAPI(route.params.applicationId);
};

const calenderPresets = [
  {
    key: "today",
    label: "Today",
    start: dayjs().startOf("day").toISOString(),
    end: dayjs().endOf("day").toISOString(),
  },
  {
    key: "yesterday",
    label: "Yesterday",
    start: dayjs().subtract(1, "day").startOf("day").toISOString(),
    end: dayjs().subtract(1, "day").endOf("day").toISOString(),
  },
  {
    key: "last_24h",
    label: "Last 24 hours",
    start: dayjs().subtract(24, "hour").toISOString(),
    end: dayjs().toISOString(),
  },
  {
    key: "last_7d",
    label: "Last 7 days",
    start: dayjs().subtract(7, "day").toISOString(),
    end: dayjs().toISOString(),
  },
  {
    key: "last_14d",
    label: "Last 14 days",
    start: dayjs().subtract(14, "day").toISOString(),
    end: dayjs().toISOString(),
  },
  {
    key: "last_30d",
    label: "Last 30 days",
    start: dayjs().subtract(30, "day").toISOString(),
    end: dayjs().toISOString(),
  },
  {
    key: "this_month",
    label: "This month",
    start: dayjs().startOf("month").toISOString(),
    end: dayjs().endOf("month").toISOString(),
  },
  {
    key: "ytd",
    label: "Year to date",
    start: dayjs().startOf("year").toISOString(),
    end: dayjs().toISOString(),
  },
  {
    key: "all_time",
    label: "All time",
    start: null,
    end: null,
  },
];

const calenderPresetSelection = ref("today");
const getCalenderPresentSelectionLabel = computed(() => {
  const preset = calenderPresets.find(
    (p) => p.key === calenderPresetSelection.value
  );
  return preset ? preset.label : "Select a preset";
});
const updateCalendderPresetSelection = (key) => {
  const preset = calenderPresets.find((p) => p.key === key);
  if (preset) {
    calenderPresetSelection.value = key;
    filters.value.start = preset.start;
    filters.value.end = preset.end;
    loadEvents();
  }
};

onMounted(() => {
  emit("currentPage", "events");

  loadEventSchema();
  loadEvents();
});
</script>

<template>
  <!-- Header -->
  <div class="mb-4 flex items-center justify-between">
    <!-- Left: Heading -->
    <h2 class="text-lg font-semibold text-gray-800">Events</h2>

    <!-- Right: Actions -->
    <div class="flex items-center gap-2">
      <!-- Refresh Button -->
      <a-button type="default" @click="loadEvents"> Refresh </a-button>

      <!-- Calendar Dropdown -->
      <a-dropdown :trigger="['click']" :overlayStyle="{ minWidth: '200px' }">
        <a-button :icon="h(CalendarOutlined)" class="inline-flex items-center">
          {{ getCalenderPresentSelectionLabel }}
        </a-button>

        <template #overlay>
          <a-menu>
            <a-menu-item
              v-for="preset in calenderPresets"
              :key="preset.key"
              @click="updateCalendderPresetSelection(preset.key)"
              :class="{
                'bg-gray-100': calenderPresetSelection === preset.key,
              }"
            >
              {{ preset.label }}
            </a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </div>
  </div>

  <!-- Table -->
  <a-table
    :columns="columns"
    :data-source="events"
    size="small"
    :pagination="false"
    :loading="loading"
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
