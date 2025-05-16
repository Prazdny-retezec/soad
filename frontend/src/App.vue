<template>
  <v-app>
    <Navbar v-if="isAuthenticated"/>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import {mapStores} from "pinia";
import {useUserStore} from "@/store/UserStore.js";

export default {
  name: 'App',
  components: {Navbar},

  computed: {
    ...mapStores(useUserStore),

    isAuthenticated() {
      return this.userStore?.isAuthenticated;
    },
  }
}

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
