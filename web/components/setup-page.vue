<script setup>
import { reactive, ref } from "vue";

// Import ONLY Ant Design Vue icons explicitly (components are provided via your global plugin)
import {
  SettingOutlined,
  HomeOutlined,
  ProfileOutlined,
  BulbOutlined,
  SafetyOutlined,
  BankOutlined,
  //   PaletteOutlined,
  FormOutlined,
  InfoCircleOutlined,
  ApartmentOutlined,
  MailOutlined,
  SaveOutlined,
  CheckCircleOutlined,
  ArrowLeftOutlined,
  UserOutlined,
  LockOutlined,
} from "@ant-design/icons-vue";

const loading = ref(false);

const orgFormRef = ref();
const adminFormRef = ref();

const org = reactive({
  organizationName: "",
  contactEmail: "",
});

const admin = reactive({
  name: "",
  email: "",
  password: "",
});

const orgRules = {
  organizationName: [
    { required: true, message: "Organization name is required" },
    { min: 2, message: "Too short" },
  ],
  contactEmail: [
    { required: true, message: "Contact email is required" },
    { type: "email", message: "Enter a valid email" },
  ],
};

const adminRules = {
  name: [{ required: true, message: "Name is required" }],
  email: [
    { required: true, message: "Email is required" },
    { type: "email", message: "Enter a valid email" },
  ],
  password: [
    { required: true, message: "Password is required" },
    { min: 8, message: "At least 8 characters" },
  ],
};

async function onSubmit() {
  try {
    loading.value = true;
    await orgFormRef.value?.validate();
    await adminFormRef.value?.validate();
    // TODO: call your APIs:
    // 1) Save org settings -> POST /api/app-settings (or /api/site-meta)
    // 2) Create superuser -> POST /api/admin/bootstrap
    // Example payloads:
    // await api.saveSettings({ organization_name: org.organizationName, organization_email: org.contactEmail })
    // await api.bootstrapAdmin({ name: admin.name, email: admin.email, password: admin.password })
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="border-b bg-white">
      <div class="mx-auto max-w-6xl px-4 py-4 flex items-center gap-3">
        <a-avatar size="large" shape="square" class="shadow-sm">
          <template #icon><SettingOutlined /></template>
        </a-avatar>
        <div class="flex-1">
          <div class="text-lg font-semibold">First-time Setup</div>
          <div class="text-gray-500 text-sm">
            Configure your application and admin.
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div
      class="mx-auto max-w-6xl px-4 py-8 grid grid-cols-1 lg:grid-cols-3 gap-6"
    >
      <!-- Left: Progress & Tips -->
      <div class="lg:col-span-1 space-y-6">
        <a-card :bordered="false" class="shadow-sm">
          <template #title>
            <div class="flex items-center gap-2">
              <BulbOutlined />
              <span>Tips</span>
            </div>
          </template>
          <div class="space-y-3 text-sm text-gray-600">
            <div class="flex items-start gap-2">
              <SafetyOutlined class="mt-0.5" />
              <span
                >Use a functional email like <b>support@yourdomain</b> for
                contact.</span
              >
            </div>
            <div class="flex items-start gap-2">
              <BankOutlined class="mt-0.5" />
              <span>Org name shows across emails and headers.</span>
            </div>
            <div class="flex items-start gap-2">
              <PaletteOutlined class="mt-0.5" />
              <span
                >Branding can be adjusted later in
                <b>Settings → Appearance</b>.</span
              >
            </div>
          </div>
        </a-card>
      </div>

      <!-- Right: Forms -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Organization Basics -->
        <a-card :bordered="false" class="shadow-sm">
          <template #title>
            <div class="flex items-center gap-2">
              <FormOutlined />
              <span>Organization Basics</span>
            </div>
          </template>

          <a-form
            ref="orgFormRef"
            :model="org"
            :rules="orgRules"
            layout="vertical"
            class="grid grid-cols-1 md:grid-cols-2 gap-4"
          >
            <a-form-item name="organizationName" label="Organization name">
              <a-input
                v-model:value="org.organizationName"
                placeholder="Acme Corp"
                allow-clear
              >
                <template #prefix><ApartmentOutlined /></template>
              </a-input>
            </a-form-item>

            <a-form-item name="contactEmail" label="Contact email">
              <a-input
                v-model:value="org.contactEmail"
                type="email"
                placeholder="support@acme.com"
                allow-clear
              >
                <template #prefix><MailOutlined /></template>
              </a-input>
            </a-form-item>
          </a-form>
        </a-card>

        <!-- Superuser Account -->
        <a-card :bordered="false" class="shadow-sm">
          <template #title>
            <div class="flex items-center gap-2">
              <UserOutlined />
              <span>Superuser Account</span>
            </div>
          </template>

          <a-form
            ref="adminFormRef"
            :model="admin"
            :rules="adminRules"
            layout="vertical"
            class="grid grid-cols-1 md:grid-cols-2 gap-4"
          >
            <a-form-item name="name" label="Full name">
              <a-input
                v-model:value="admin.name"
                placeholder="Jane Doe"
                allow-clear
              >
                <template #prefix><UserOutlined /></template>
              </a-input>
            </a-form-item>

            <a-form-item name="email" label="Admin email">
              <a-input
                v-model:value="admin.email"
                type="email"
                placeholder="admin@acme.com"
                allow-clear
              >
                <template #prefix><MailOutlined /></template>
              </a-input>
            </a-form-item>

            <a-form-item name="password" label="Password" class="md:col-span-2">
              <a-input-password
                v-model:value="admin.password"
                placeholder="At least 8 characters"
              >
                <template #prefix><LockOutlined /></template>
              </a-input-password>
            </a-form-item>

            <a-button type="primary" :loading="loading" @click="onSubmit">
              <CheckCircleOutlined />
              <span class="ml-1">Complete setup</span>
            </a-button>
          </a-form>
        </a-card>
      </div>
    </div>
  </div>
</template>
