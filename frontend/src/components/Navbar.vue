<template>
  <nav>
    <v-app-bar flat color="dark-green">

      <v-app-bar-title class="mx-4 hidden-md-and-down">
        <h1 class="text-h5 font-weight-bold nav_element">
          <router-link :to="{'name': 'measurement-list'}">
            SOAD System
          </router-link>
        </h1>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <div class="hidden-sm-and-down d-flex">
        <v-btn :to="{ name: 'measurement-list' }" class="mr-2 text-caption">
          <span class="nav_element">Measurements</span>
        </v-btn>
        <v-btn :to="{ name: 'sensor-settings' }" class="mx-2 text-caption">
          <span class="nav_element">Sensor settings</span>
        </v-btn>
      </div>

      <v-menu anchor="bottom end" v-model="userMenuShown">
        <template v-slot:activator="{ props }">
          <v-btn color="black" icon="mdi-account-circle" v-bind="props"></v-btn>
        </template>
        <v-list>
          <v-list-item v-if="isAuthenticated" @click="logout()">
            <v-list-item-title>Log out</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  </nav>
</template>

<script>
import {useUserStore} from '@/store/UserStore';
import {mapStores} from 'pinia';

export default {
  name: 'Navbar',

  data() {
    return {
      userMenuShown: false,
    };
  },

  computed: {
    ...mapStores(useUserStore),

    isAuthenticated() {
      return useUserStore().isAuthenticated;
    },
  },

  methods: {
    logout() {
      useUserStore().logout();
      this.$router.push({name: 'login'});
      this.userMenuShown = false;
    }
  },
};
</script>

<style>
.nav_element {
  font-family: "Outfit", sans-serif;
  font-size: 14px;
  line-height: 27px;
  color: #323232;
  text-transform: capitalize;
  font-weight: normal;
}
</style>
