<!-- PropertyFilter.vue -->
<script setup>
import { ref, computed, watch } from "vue";

const emit = defineEmits(["add"]);

const property = ref("");
const operator = ref("eq");
const query = ref("");

const isNumeric = computed(() => ["lt", "gt"].includes(operator.value));

watch(operator, () => {
  if (isNumeric.value && query.value && isNaN(Number(query.value))) {
    query.value = "";
  }
});

const canAdd = computed(
  () =>
    property.value.trim().length > 0 &&
    operator.value &&
    query.value.trim().length > 0
);

function onAdd() {
  if (!canAdd.value) return;

  const additionalFilter = {
    key: property.value.trim(),
    operator: operator.value,
    value: isNumeric.value ? Number(query.value) : query.value.trim(),
  };

  emit("add", additionalFilter);
  property.value = "";
  query.value = "";
  operator.value = "eq";
}
</script>

<template>
  <div class="w-full">
    <div class="grid grid-cols-12 gap-2 items-center">
      <!-- Property -->
      <div class="col-span-4">
        <a-input
          v-model:value="property"
          allow-clear
          placeholder="Property"
          class="w-full"
          size="small"
        />
      </div>

      <!-- Operator -->
      <div class="col-span-4">
        <a-select
          v-model:value="operator"
          size="small"
          class="w-full"
          :options="[
            { label: 'equals', value: 'eq' },
            { label: 'less than', value: 'lt' },
            { label: 'greater than', value: 'gt' },
            { label: 'not equal', value: 'neq' },
            { label: 'contains', value: 'contains' },
            { label: 'does not contain', value: 'not_contains' },
          ]"
        />
      </div>

      <!-- Value -->
      <div class="col-span-3">
        <a-input
          v-model:value="query"
          :type="isNumeric ? 'number' : 'text'"
          allow-clear
          placeholder="Value"
          class="w-full"
          size="small"
          @keydown.enter.prevent="onAdd"
        />
      </div>

      <!-- Add -->
      <div class="col-span-1">
        <a-button
          type="primary"
          size="small"
          :disabled="!canAdd"
          class="w-full"
          @click="onAdd"
        >
          Add
        </a-button>
      </div>
    </div>
  </div>
</template>
