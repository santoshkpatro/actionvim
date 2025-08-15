<script setup>
import { ref } from "vue";
import {
  SettingOutlined,
  BulbOutlined,
  SafetyOutlined,
  BankOutlined,
  BgColorsOutlined,
  FormOutlined,
  ApartmentOutlined,
  MailOutlined,
  CheckCircleOutlined,
  UserOutlined,
  LockOutlined,
  GlobalOutlined,
} from "@ant-design/icons-vue";
import { updateSiteMeta } from "@/api";

const loading = ref(false);
const formRef = ref();

// flat fields, using a single ref
const formFields = ref({
  organizationName: "",
  organizationContactEmail: "",
  organizationWebsite: "",
  superuserFullName: "",
  superuserEmail: "",
  superuserPassword: "",
});

async function onSubmit() {
  try {
    loading.value = true;
    await formRef.value?.validate();
    await updateSiteMeta(formFields.value);
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
      <!-- Left: Tips -->
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
              <BgColorsOutlined class="mt-0.5" />
              <span
                >Branding can be adjusted later in
                <b>Settings → Appearance</b>.</span
              >
            </div>
          </div>
        </a-card>
      </div>

      <!-- Right: Single Form -->
      <div class="lg:col-span-2">
        <a-card :bordered="false" class="shadow-sm">
          <template #title>
            <div class="flex items-center gap-2">
              <FormOutlined />
              <span>Setup Details</span>
            </div>
          </template>

          <a-form
            ref="formRef"
            :model="formFields"
            name="setupForm"
            layout="vertical"
            autocomplete="off"
            class="grid grid-cols-1 md:grid-cols-2 gap-4"
            @finish="onSubmit"
          >
            <!-- Organization -->
            <div class="md:col-span-2">
              <div class="text-sm font-semibold text-gray-700 mb-2">
                Organization
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <a-form-item
                  name="organizationName"
                  label="Organization name"
                  :rules="[
                    {
                      required: true,
                      message: 'Organization name is required',
                    },
                    {
                      min: 2,
                      message: 'Too short',
                    },
                  ]"
                  validateTrigger="blur"
                >
                  <a-input
                    v-model:value="formFields.organizationName"
                    placeholder="Acme Corp"
                    allow-clear
                  >
                    <template #prefix><ApartmentOutlined /></template>
                  </a-input>
                </a-form-item>

                <a-form-item
                  name="organizationContactEmail"
                  label="Contact email"
                  :rules="[
                    {
                      type: 'email',
                      message: 'Please enter a valid email',
                    },
                    {
                      required: true,
                      message: 'Contact email is required',
                    },
                  ]"
                  validateTrigger="blur"
                >
                  <a-input
                    v-model:value="formFields.organizationContactEmail"
                    type="email"
                    placeholder="support@acme.com"
                    allow-clear
                    :rules="[
                      { required: true, message: 'Contact email is required' },
                      { type: 'email', message: 'Please enter a valid email' },
                    ]"
                    validateTrigger="blur"
                  >
                    <template #prefix><MailOutlined /></template>
                  </a-input>
                </a-form-item>

                <a-form-item
                  name="organizationWebsite"
                  label="Website"
                  :rules="[
                    { type: 'url', message: 'Please enter a valid URL' },
                  ]"
                  validateTrigger="blur"
                >
                  <a-input
                    v-model:value="formFields.organizationWebsite"
                    placeholder="https://acme.com"
                    allow-clear
                  >
                    <template #prefix><GlobalOutlined /></template>
                  </a-input>
                </a-form-item>
              </div>
            </div>

            <!-- Superuser -->
            <div class="md:col-span-2 mt-2">
              <div class="text-sm font-semibold text-gray-700 mb-2">
                Superuser
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <a-form-item
                  name="superuserFullName"
                  label="Full name"
                  :rules="[
                    { required: true, message: 'Full name is required' },
                    { min: 2, message: 'Too short' },
                  ]"
                  validateTrigger="blur"
                >
                  <a-input
                    v-model:value="formFields.superuserFullName"
                    placeholder="Jane Doe"
                    allow-clear
                  >
                    <template #prefix><UserOutlined /></template>
                  </a-input>
                </a-form-item>

                <a-form-item
                  name="superuserEmail"
                  label="Email"
                  :rules="[
                    { required: true, message: 'Admin email is required' },
                    { type: 'email', message: 'Please enter a valid email' },
                  ]"
                  validateTrigger="blur"
                >
                  <a-input
                    v-model:value="formFields.superuserEmail"
                    type="email"
                    placeholder="admin@acme.com"
                    allow-clear
                  >
                    <template #prefix><MailOutlined /></template>
                  </a-input>
                </a-form-item>

                <a-form-item
                  name="superuserPassword"
                  label="Password"
                  class="md:col-span-2"
                  :rules="[
                    { required: true, message: 'Password is required' },
                    {
                      min: 8,
                      message: 'Password must be at least 8 characters',
                    },
                  ]"
                  validateTrigger="blur"
                >
                  <a-input-password
                    v-model:value="formFields.superuserPassword"
                    placeholder="At least 8 characters"
                    autocomplete="new-password"
                    allow-clear
                  >
                    <template #prefix><LockOutlined /></template>
                  </a-input-password>
                </a-form-item>
              </div>
            </div>

            <!-- Submit -->
            <div class="md:col-span-2">
              <a-button type="primary" :loading="loading" html-type="submit">
                <CheckCircleOutlined />
                <span class="ml-1">Complete setup</span>
              </a-button>
            </div>
          </a-form>
        </a-card>
      </div>
    </div>
  </div>
</template>
