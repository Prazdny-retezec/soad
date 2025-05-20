import {defineStore} from "pinia";

export const useUserStore = defineStore('user', {
    state: () => ({
        isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
        error: null,
        isLoggingIn: false,
        loginMessage: null,
        afterLoginRoute: null,
        users: [],
        isLoading: false
      }),


    actions: {
        login() {
          this.isAuthenticated = true;
          localStorage.setItem('isAuthenticated', 'true'); 
        },
        
        logout() {
          this.isAuthenticated = false;
          localStorage.removeItem('isAuthenticated'); 
        },
    }
})