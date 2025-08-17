<script setup>
import { ref, computed } from "vue";
import { message } from "ant-design-vue";
import { Copy } from "lucide-vue-next";

const props = defineProps({
  properties: {
    type: Object,
    required: true,
  },
});

const activeKey = ref("properties");

/* Build [key, value] pairs once, sorted by key */
const kvList = computed(() =>
  Object.entries(props.properties || {}).sort(([a], [b]) => a.localeCompare(b))
);

function formatValue(v) {
  if (v === null) return "null";
  if (v === undefined) return "undefined";
  if (typeof v === "object") {
    try {
      return JSON.stringify(v);
    } catch {
      return "[object]";
    }
  }
  return String(v);
}

const prettyJSON = computed(() =>
  JSON.stringify(props.properties || {}, null, 2)
);
</script>

<template>
  <a-tabs v-model:activeKey="activeKey">
    <a-tab-pane key="properties" tab="Properties">
      <a-list :data-source="kvList" item-layout="horizontal" class="mt-2">
        <template #renderItem="{ item }">
          <!-- item is [key, value] -->
          <a-list-item class="!px-2 !py-1">
            <div
              class="grid grid-cols-[1fr_2fr_auto] items-center gap-3 w-full"
            >
              <!-- Key (left) -->
              <div class="text-[13px] text-gray-600 truncate" :title="item[0]">
                {{ item[0] }}
              </div>

              <!-- Value (middle) -->
              <div
                class="text-[13px] text-gray-900 truncate"
                :title="formatValue(item[1])"
              >
                {{ formatValue(item[1]) }}
              </div>

              <!-- Copy (right) -->
              <a-tooltip title="Copy value">
                <Copy class="w-4 h-4 text-gray-700" />
              </a-tooltip>
            </div>
          </a-list-item>
        </template>
      </a-list>
    </a-tab-pane>

    <a-tab-pane key="json" tab="JSON">
      <pre
        class="mt-2 bg-gray-50 border border-gray-200 rounded-lg p-2 text-xs overflow-auto"
        >{{ prettyJSON }}</pre
      >
    </a-tab-pane>
  </a-tabs>
</template>
