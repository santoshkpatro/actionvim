<template>
  <div class="min-h-screen grid place-items-center bg-white">
    <div class="w-full max-w-md px-6">
      <!-- Brand / Logo -->
      <div class="mb-8 text-center">
        <div
          class="inline-flex items-center justify-center w-11 h-11 rounded-2xl bg-gray-100 border border-gray-200 shadow-sm"
          :title="orgName"
          aria-label="Brand"
        >
          <span class="text-lg font-semibold">{{ brandInitials }}</span>
        </div>
        <h1 class="mt-4 text-2xl font-semibold tracking-tight">
          Sign in to {{ orgName }}
        </h1>
      </div>

      <!-- Login Card -->
      <div class="rounded-2xl border border-gray-200 shadow-sm p-6">
        <a-form
          :model="form"
          layout="vertical"
          @finish="onFinish"
          @finishFailed="onFinishFailed"
          hide-required-mark
        >
          <a-form-item
            name="email"
            label="Email"
            :rules="[
              { required: true, message: 'Please enter your email' },
              { type: 'email', message: 'Enter a valid email' },
            ]"
            validateTrigger="blur"
          >
            <a-input
              v-model:value="form.email"
              placeholder="name@company.com"
            />
          </a-form-item>

          <a-form-item
            name="password"
            label="Password"
            :rules="[{ required: true, message: 'Please enter your password' }]"
            validateTrigger="blur"
          >
            <a-input-password
              v-model:value="form.password"
              placeholder="••••••••"
            />
          </a-form-item>

          <div class="flex items-center justify-between mb-3">
            <a-checkbox v-model:checked="form.remember">Remember me</a-checkbox>

            <!-- Tailwind-styled anchor instead of Ant Typography -->
            <a
              href="#"
              class="text-sm underline text-gray-500 hover:text-gray-700"
              @click.prevent="onForgot"
            >
              Forgot password?
            </a>
          </div>

          <a-button
            html-type="submit"
            type="primary"
            block
            :loading="submitting"
          >
            Sign in
          </a-button>
        </a-form>
      </div>

      <!-- Footer / Help -->
      <div class="mt-8 text-center text-xs text-gray-400 space-y-2">
        <div>
          By continuing, you agree to our
          <a class="underline hover:text-gray-600" href="#">Terms</a> and
          <a class="underline hover:text-gray-600" href="#">Privacy Policy</a>.
        </div>
        <div>
          Need help?
          <a
            class="underline hover:text-gray-600"
            :href="`mailto:${supportEmail}`"
          >
            {{ supportEmail }}
          </a>
        </div>
        <div class="pt-1">
          Powered by <span class="font-medium text-gray-500">ActionVim</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from "vue";
import { useStore } from "@/store";

const store = useStore();

const submitting = ref(false);
const form = reactive({
  email: "",
  password: "",
  remember: true,
});

const rules = {
  email: [
    { required: true, message: "Please enter your email" },
    { type: "email, message: 'Enter a valid email'" },
  ],
  password: [
    { required: true, message: "Please enter your password" },
    { min: 6, message: "Minimum 6 characters" },
  ],
};

// Org/support from Pinia with fallbacks
const orgName = computed(() => store.siteMeta?.organizationName || "ActionVim");
const supportEmail = computed(
  () => store.siteMeta?.organizationContactEmail || "support@actionvim.com"
);

// Brand initials
const brandInitials = computed(() => {
  const name = (orgName.value || "").trim();
  const letters = name.match(/\b[A-Za-z]/g);
  return (letters?.slice(0, 2).join("") || "AV").toUpperCase();
});

const onFinish = async () => {
  try {
    submitting.value = true;
    // await api.post('/api/auth/login', form)
    // router.push({ name: 'dashboard' })
    console.log("Form submitted:", form);
  } finally {
    submitting.value = false;
  }
};

const onFinishFailed = () => {};
const onForgot = () => {
  // router.push({ name: 'forgot-password' })
};
</script>

<style scoped></style>
