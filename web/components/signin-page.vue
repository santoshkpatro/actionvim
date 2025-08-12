<template>
  <div class="min-h-screen grid place-items-center bg-white">
    <div class="w-full max-w-md px-6">
      <!-- Brand / Logo -->
      <div class="mb-8 text-center">
        <div
          class="inline-flex items-center justify-center w-11 h-11 rounded-2xl bg-gray-100 border border-gray-200 shadow-sm"
        >
          <span class="text-lg font-semibold">AV</span>
        </div>
        <h1 class="mt-4 text-2xl font-semibold tracking-tight">
          Sign in to ActionVim
        </h1>
      </div>

      <!-- Login Card -->
      <div class="rounded-2xl border border-gray-200 shadow-sm p-6">
        <a-form
          :model="form"
          :rules="rules"
          layout="vertical"
          @finish="onFinish"
          @finishFailed="onFinishFailed"
          hide-required-mark
        >
          <a-form-item name="email" label="Email">
            <a-input
              v-model:value="form.email"
              placeholder="name@company.com"
            />
          </a-form-item>

          <a-form-item name="password" label="Password">
            <a-input-password
              v-model:value="form.password"
              placeholder="••••••••"
            />
          </a-form-item>

          <div class="flex items-center justify-between mb-3">
            <a-checkbox v-model:checked="form.remember">Remember me</a-checkbox>
            <a-typography-link @click.prevent="onForgot" class="text-sm"
              >Forgot password?</a-typography-link
            >
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
      <div class="mt-8 text-center text-xs text-gray-400">
        By continuing, you agree to our
        <a class="underline hover:text-gray-600" href="#">Terms</a> and
        <a class="underline hover:text-gray-600" href="#">Privacy Policy</a>.
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";

// Ant Design Vue components are globally registered via your plugin setup.
// This file intentionally avoids local imports.

const submitting = ref(false);
const form = reactive({
  email: "",
  password: "",
  remember: true,
});

const rules = {
  email: [
    { required: true, message: "Please enter your email" },
    { type: "email", message: "Enter a valid email" },
  ],
  password: [
    { required: true, message: "Please enter your password" },
    { min: 6, message: "Minimum 6 characters" },
  ],
};

const onFinish = async () => {
  try {
    submitting.value = true;
    // TODO: call your auth API here
    // await api.post('/api/auth/login', form)
    // On success, route to your app dashboard
    // router.push({ name: 'dashboard' })
  } finally {
    submitting.value = false;
  }
};

const onFinishFailed = () => {
  // Optional: you can show a message or focus the first invalid field
};

const onForgot = () => {
  // router.push({ name: 'forgot-password' })
};

const onSignup = () => {
  // router.push({ name: 'register' })
};
</script>

<style scoped></style>
