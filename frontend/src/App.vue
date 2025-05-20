<template>
  <v-app>
    <Navbar v-if="userStore.isAuthenticated" />

    <v-main>

      <ErrorDialog
        v-model="uiStore.authError"
        title="Authentication Mismatch"
        message="Frontend and backend credentials don’t match. Please check your .env settings."
        @close="uiStore.clearAuthError"
      />

      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Navbar      from "@/components/Navbar.vue";
import ErrorDialog from "@/components/ErrorDialog.vue";
import { mapStores } from "pinia";
import { useUserStore } from "@/store/UserStore.js";
import { useUiStore }   from "@/store/Ui.js";

export default {
  name: "App",
  components: { Navbar, ErrorDialog },
  computed: {
    ...mapStores(useUserStore, useUiStore),
    isAuthenticated() {
      return this.userStore.isAuthenticated;
    },
  },
};
</script>


<style>
a, a:hover, a:visited {
  text-decoration: none;
  color: #323232;
}

.body_text {
  font-family: "Roboto", sans-serif;
  font-size: 16px;
  line-height: 27px;
  color: #323232;
}

.subtitle {
  font-family: "Roboto", sans-serif;
  font-size: 20px;
  line-height: 27px;
  color: #323232;
  font-weight: bolder;
  letter-spacing: 1px;
}

.filter_wrapper {
  min-height: 2rem;
  box-sizing: border-box;
  border-bottom: 1px solid #E3E0DF;
  position: sticky;
}

.rotate-180 {
  transform: rotate(180deg);
}

.new_measurement {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex: 1;
}

</style>
