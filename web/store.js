import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { getMe } from "@/api";

export const useStore = defineStore("store", () => {
  const loggedInUser = ref(null);
  const isAuthenticated = computed(() => !!loggedInUser.value);

  const setLoggedInUser = async () => {
    try {
      const { data } = await getMe();
      if (data.is_authenticated) {
        loggedInUser.value = data.user;
      } else {
        loggedInUser.value = null;
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
      loggedInUser.value = null;
    }
  };

  const clearLoggedInUser = () => {
    loggedInUser.value = null;
  };

  return {
    loggedInUser,
    isAuthenticated,
    setLoggedInUser,
    clearLoggedInUser,
  };
});
