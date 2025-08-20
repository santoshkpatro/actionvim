<script setup>
/* ===== Imports ===== */
import { eventsListAPI, eventsSchemaAPI } from "@/api";
import { ref, onMounted, h, computed } from "vue";
import { useRoute } from "vue-router";
import { Menu } from "lucide-vue-next";
import {
  CalendarOutlined,
  PlusOutlined,
  CloseOutlined,
} from "@ant-design/icons-vue";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
dayjs.extend(relativeTime);

/* ===== Emits / Child Components ===== */
const emit = defineEmits(["currentPage"]);
import EventProperties from "@/components/application/event-properties.vue";
import EventFilter from "@/components/application/event-filter.vue";

/* ===== Table Columns ===== */
const columns = [
  { key: "name", title: "Event", dataIndex: "name" },
  { key: "capturedAt", title: "Time" },
  { key: "source", title: "Source", dataIndex: "source" },
  { key: "action", width: 75 },
];

/* ===== State ===== */
const loading = ref(false);
const route = useRoute();
const events = ref([]);
const schema = ref({ eventNames: [] });

/* filters.properties uses [{ key, operator, value }] */
const filters = ref({
  start: dayjs().startOf("day").toISOString(),
  end: dayjs().endOf("day").toISOString(),
  name: null,
  properties: [],
});

/* Calendar presets */
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
  { key: "all_time", label: "All time", start: null, end: null },
];
const calenderPresetSelection = ref("today");

/* ===== Computed ===== */
const getCalenderPresentSelectionLabel = computed(() => {
  const p = calenderPresets.find(
    (x) => x.key === calenderPresetSelection.value
  );
  return p ? p.label : "Select a preset";
});

/* ===== Methods (grouped) ===== */
// API
const loadEvents = async () => {
  console.log("Filters:", filters.value);

  loading.value = true;
  const recent = await eventsListAPI(route.params.applicationId, filters.value);
  events.value = recent.map((e) => ({ ...e, key: e.id }));
  loading.value = false;
};
const loadEventSchema = async () => {
  schema.value = await eventsSchemaAPI(route.params.applicationId);
};

// Calendar handlers
const updateCalendderPresetSelection = (key) => {
  const p = calenderPresets.find((x) => x.key === key);
  if (!p) return;
  calenderPresetSelection.value = key;
  filters.value.start = p.start;
  filters.value.end = p.end;
  loadEvents();
};

// Event-name filter
const updateEventFilter = (eventName) => {
  filters.value.name = eventName;
  loadEvents();
};

// Property filters (key, operator, value)
const operatorText = {
  eq: "=",
  lt: "<",
  gt: ">",
  neq: "≠",
  contains: "contains",
  not_contains: "doesn't contain",
};
const summarizeFilter = (f) => {
  const op = operatorText[f.operator] ?? f.operator;
  const val = typeof f.value === "string" ? `"${f.value}"` : f.value;
  return `${f.key} ${op} ${val}`;
};

// Add/replace by unique `key`
const openFilter = ref(false);
const showFilter = () => {
  openFilter.value = true;
};
const addPropertyFilter = (f /* { key, operator, value } */) => {
  const idx = filters.value.properties.findIndex((x) => x.key === f.key);
  if (idx === -1) filters.value.properties.push({ ...f });
  else filters.value.properties.splice(idx, 1, { ...f }); // replace existing
  openFilter.value = false;
  loadEvents();
};

// Remove by key
const removePropertyFilter = (key) => {
  const i = filters.value.properties.findIndex((x) => x.key === key);
  if (i !== -1) {
    filters.value.properties.splice(i, 1);
    loadEvents();
  }
};

// Clear all
const clearAllPropertyFilters = () => {
  if (filters.value.properties.length) {
    filters.value.properties = [];
    loadEvents();
  }
};

/* ===== Lifecycle ===== */
onMounted(() => {
  emit("currentPage", "events");
  loadEventSchema();
  loadEvents();
});
</script>

<template>
  <!-- Header -->
  <div class="mb-2 flex items-center justify-between">
    <h2 class="text-lg font-semibold text-gray-800">Events</h2>

    <div class="flex items-center gap-2">
      <a-button type="default" @click="loadEvents">Refresh</a-button>

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
              :class="{ 'bg-gray-100': calenderPresetSelection === preset.key }"
            >
              {{ preset.label }}
            </a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </div>
  </div>

  <!-- Filters Row -->
  <div class="mb-3 flex flex-wrap items-center gap-2">
    <!-- Select event -->
    <a-dropdown :trigger="['click']" :overlayStyle="{ minWidth: '200px' }">
      <a-button>{{ filters?.name || "Select an event" }}</a-button>
      <template #overlay>
        <a-menu>
          <a-menu-item
            v-for="eventName in schema.eventNames"
            :key="eventName"
            @click="updateEventFilter(eventName)"
            :class="{ 'bg-gray-100': filters.name === eventName }"
          >
            {{ eventName }}
          </a-menu-item>
        </a-menu>
      </template>
    </a-dropdown>

    <!-- Property filter buttons (pill + cross icon) -->
    <div
      v-if="filters.properties.length"
      class="flex flex-wrap items-center gap-2"
    >
      <a-button
        v-for="f in filters.properties"
        :key="f.key"
        size="small"
        type="default"
        class="!m-0 inline-flex items-center gap-1 rounded-full !px-2 !h-7"
        @click="removePropertyFilter(f.key)"
      >
        <span class="text-xs">{{ summarizeFilter(f) }}</span>
        <CloseOutlined class="text-gray-500" />
      </a-button>

      <a-button
        type="link"
        size="small"
        class="!px-1 !h-auto text-xs"
        @click="clearAllPropertyFilters"
      >
        Clear all
      </a-button>
    </div>

    <!-- Add Filter -->
    <a-dropdown
      :trigger="['click']"
      :overlayStyle="{ maxWidth: '600px' }"
      v-model:open="openFilter"
      destroyPopupOnHide
    >
      <a-button :icon="h(PlusOutlined)" type="dashed" @click="showFilter">
        Add Filter
      </a-button>
      <template #overlay>
        <a-card size="small">
          <!-- Child should emit { key, operator, value } -->
          <event-filter @add="addPropertyFilter" />
        </a-card>
      </template>
    </a-dropdown>
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
        <Menu class="w-4 h-4" />
      </template>
    </template>

    <template #expandedRowRender="{ record }">
      <event-properties :properties="JSON.parse(record.properties)" />
    </template>
  </a-table>
</template>
