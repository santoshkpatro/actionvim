import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { getMe, getSiteMeta } from "@/api";

export const useStore = defineStore("store", () => {
  const siteMeta = ref(null);
  const isSiteMetaLoaded = computed(() => !!siteMeta.value);

  const loggedInUser = ref(null);
  const isAuthenticated = computed(() => !!loggedInUser.value);

  const loadSiteMeta = async () => {
    try {
      const siteData = await getSiteMeta();
      if (!siteData.isReady) {
        console.warn("Site is not ready yet.");
      }
      siteMeta.value = siteData.meta;
    } catch (error) {
      console.error("Error loading site meta:", error);
      siteMeta.value = null;
    }
  };

  const setLoggedInUser = async () => {
    try {
      const authStatus = await getMe();
      if (authStatus.authenticated) {
        loggedInUser.value = authStatus.user;
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
    siteMeta,
    isSiteMetaLoaded,
    loadSiteMeta,
  };
});
