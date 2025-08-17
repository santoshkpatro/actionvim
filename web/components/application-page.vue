<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "@/store";

// Lucide icons
import {
  LayoutDashboard,
  Eye,
  Zap,
  IdCard,
  Users,
  Layers,
  Settings,
  UserCircle,
  Star,
  Mail,
  HelpCircle,
  BookOpenText,
  ChevronDown,
  CircleDot,
  Plus,
} from "lucide-vue-next";
import { applicationsListAPI } from "@/api";

const route = useRoute();
const router = useRouter();
const store = useStore();

/* ===== Brand / org ===== */
const brandName = computed(() => store?.siteMeta?.organizationName || "Micron");
const logoUrl = computed(
  () => store?.siteMeta?.organizationLogo || store?.siteMeta?.logoUrl || ""
);

/* ===== Nav ===== */
const primaryItems = [
  {
    key: "dashboard",
    label: "Dashboard",
    to: `/application/${route.params.applicationId}`,
    icon: LayoutDashboard,
  },
  {
    key: "views",
    label: "Views",
    to: `/application/${route.params.applicationId}/views`,
    icon: Eye,
  },
  {
    key: "events",
    label: "Events",
    to: `/application/${route.params.applicationId}/events`,
    icon: Zap,
  },
  {
    key: "identities",
    label: "Identities",
    to: `/application/${route.params.applicationId}/identities`,
    icon: IdCard,
  },
  {
    key: "people",
    label: "People",
    to: `/application/${route.params.applicationId}/people`,
    icon: Users,
  },
  {
    key: "cohorts",
    label: "Cohorts",
    to: `/application/${route.params.applicationId}/cohorts`,
    icon: Layers,
  },
  {
    key: "settings",
    label: "Settings",
    to: `/application/${route.params.applicationId}/settings`,
    icon: Settings,
  },
];

const supportEmail = computed(
  () => store?.siteMeta?.supportEmail || "support@actionvim.com"
);
const githubUrl = computed(
  () => store?.siteMeta?.githubUrl || "https://github.com/actionvim"
);
const secondaryItems = computed(() => [
  {
    key: "github",
    label: "Star us on Github",
    href: githubUrl.value,
    icon: Star,
  },
  {
    key: "support",
    label: "Support",
    href: `mailto:${supportEmail.value}`,
    icon: Mail,
  },
  { key: "help", label: "Help", to: "/help", icon: HelpCircle },
  { key: "docs", label: "Documentation", to: "/docs", icon: BookOpenText },
]);

/* ===== Applications (for dropdown) ===== */
const applications = computed(() => store?.applications || []);
const currentApplication = computed(() => store?.currentApplication || null);

async function go(to) {
  if (to && route.path !== to) await router.push(to);
}

const loadAndSetCurrentApplication = async () => {
  const apps = await applicationsListAPI();
  store.setApplications(apps);

  const found = apps.find((app) => app.id === route.params.applicationId);
  if (!found) return router.push({ name: "not-found" });
  store.setCurrentApplication(found);
};

function onAppMenuClick({ key }) {
  if (key === "__all__") {
    router.push({ path: "/application/create" });
    return;
  }
  const app = applications.value.find((a) => String(a.id) === String(key));
  if (app) {
    store.setCurrentApplication(app);
    router.push({ path: `/application/${app.id}` });
  }
}

onMounted(() => {
  loadAndSetCurrentApplication();
});

/* ===== Active page highlight ===== */
const currentPage = ref("");
const setCurrentPage = (pageName) => {
  currentPage.value = pageName;
};
function isActive(navKey) {
  return navKey === currentPage.value;
}
</script>

<template>
  <div class="flex h-screen bg-gray-50 text-gray-900">
    <!-- Sidebar -->
    <aside
      class="w-56 h-full sticky top-0 bg-white border-r border-gray-200 flex flex-col select-none"
      aria-label="Primary"
    >
      <!-- Brand: Logo (left) + Text (right) -->
      <div class="px-2 py-2">
        <div class="flex items-center gap-2">
          <!-- Logo -->
          <div
            class="w-7 h-7 rounded-xl bg-gray-100 border border-gray-200 overflow-hidden grid place-items-center"
          >
            <img
              v-if="logoUrl"
              :src="logoUrl"
              alt="Logo"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-[11px] font-semibold text-gray-700">
              {{ brandName.slice(0, 2).toUpperCase() }}
            </span>
          </div>

          <!-- Text -->
          <span
            class="text-sm font-semibold tracking-tight text-gray-800 truncate"
          >
            {{ brandName }}
          </span>
        </div>
      </div>

      <!-- Primary nav (scrollable) -->
      <nav
        class="mt-1 flex-1 overflow-y-auto"
        role="navigation"
        aria-label="Main"
      >
        <ul class="px-1.5 space-y-1">
          <li v-for="item in primaryItems" :key="item.key">
            <a
              :href="item.to"
              class="no-underline group flex items-center gap-2 rounded-lg px-2 py-1.5 text-[13px] font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900"
              :class="isActive(item.key) ? 'bg-gray-100 text-gray-900' : ''"
              @click.prevent="go(item.to)"
            >
              <component
                :is="item.icon"
                class="shrink-0 w-[17px] h-[17px]"
                :class="
                  isActive(item.key)
                    ? 'text-indigo-600'
                    : 'text-gray-600 group-hover:text-gray-800'
                "
              />
              <span class="truncate">{{ item.label }}</span>
            </a>
          </li>
        </ul>
      </nav>

      <!-- Secondary items (just above footer, not in scroll area) -->
      <nav class="border-t border-gray-200" aria-label="Secondary">
        <ul class="px-1.5 py-2 space-y-1">
          <li v-for="item in secondaryItems" :key="item.key">
            <a
              :href="item.href || item.to || '#'"
              :target="item.href ? '_blank' : undefined"
              :rel="item.href ? 'noopener' : undefined"
              class="no-underline group flex items-center gap-2 rounded-lg px-2 py-1.5 text-[13px] text-gray-700 hover:bg-gray-50 hover:text-gray-900"
              @click.prevent="item.to ? go(item.to) : undefined"
            >
              <component
                :is="item.icon"
                class="shrink-0 w-[17px] h-[17px] text-gray-600 group-hover:text-gray-800"
              />
              <span class="truncate">{{ item.label }}</span>
            </a>
          </li>
        </ul>
      </nav>

      <!-- Footer -->
      <footer class="mt-auto border-t border-gray-200">
        <div class="h-10 px-2 text-[12px] text-gray-500 flex items-center">
          <span>Powered by</span>
          <span class="ml-1 font-medium text-gray-700">Actionvim</span>
        </div>
      </footer>
    </aside>

    <!-- Content area with Topbar -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Topbar: App dropdown (left), profile (right) -->
      <div
        class="h-12 bg-white border-b border-gray-200 px-2 flex items-center gap-2"
      >
        <!-- App selector -->
        <a-dropdown trigger="['click']">
          <div
            class="inline-flex items-center gap-1.5 px-2 py-1.5 text-[13px] font-medium text-gray-700 cursor-pointer"
            aria-label="Select application"
          >
            <span class="truncate max-w-[220px]">
              {{ currentApplication?.name || "Select application" }}
            </span>
            <ChevronDown class="w-4 h-4 text-gray-600" />
          </div>

          <template #overlay>
            <a-menu @click="onAppMenuClick">
              <a-menu-item
                v-for="app in applications"
                :key="app.id"
                :title="app.name"
              >
                <div class="flex items-center justify-between">
                  <span class="truncate">{{ app.name }}</span>

                  <!-- Active app indicator -->
                  <circle-dot
                    v-if="
                      currentApplication && currentApplication.id === app.id
                    "
                    class="w-2 h-2"
                    fill="currentColor"
                  ></circle-dot>
                </div>
              </a-menu-item>
              <a-menu-divider />
              <a-menu-item key="__all__">
                <div class="inline-flex items-center gap-1">
                  <plus class="h-4 w-4"></plus>
                  <span>Create new application</span>
                </div>
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>

        <!-- Spacer pushes profile to right -->
        <div class="flex-1"></div>

        <!-- Profile icon -->
        <button
          class="inline-flex items-center justify-center rounded-lg p-1.5 hover:bg-gray-50"
          aria-label="Profile"
          @click="go('/profile')"
        >
          <UserCircle class="w-5 h-5 text-gray-700" />
        </button>
      </div>

      <!-- Main content -->
      <main class="flex-1 overflow-y-auto p-4">
        <router-view
          @currentPage="setCurrentPage"
          :key="route.params.applicationId"
        />
      </main>
    </div>
  </div>
</template>

<style scoped>
:global(::-webkit-scrollbar) {
  width: 6px;
  height: 6px;
}
:global(::-webkit-scrollbar-thumb) {
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.08);
}
</style>
