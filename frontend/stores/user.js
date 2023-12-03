import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const isLoggedIn = computed(() => !!user.value)

  function setUser(newUserData) {
    user.value = newUserData
  }

  return { user, isLoggedIn, setUser }
})
