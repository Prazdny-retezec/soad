import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', {
  state: () => ({
    authError: false
  }),
  actions: {
    clearAuthError() {
      this.authError = false
    }
  }
})