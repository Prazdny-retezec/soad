<template>
  <v-container fluid fill-height class="ma-0 pa-0">
    <div class="fullscreen-image pt-16">
      <v-row align="center" justify="center" fill-height class="mt-20">
        <!-- Empty Column -->
        <v-col cols="6"></v-col>

        <!-- Title Column -->
        <v-col cols="6">
          <div class="landing_page_title">
            <span>SOAD </span><br>
            <span class="pl-8">system</span>
          </div>

          <div align="center" class="mt-10 mr-16">
            <!-- Login form -->
            <v-card class="mx-auto my-8"
                    variant="tonal"
                    height="300px"
                    width="420px"
                    color="card_color-darken-4"
                    rounded="xl"
                    style="display:flex;
                    flex-direction:column">
              <v-form class="mx-4" v-model="formValid" lazy-validation ref="form" align="center" justify="center">
                <!-- Username -->
                <v-text-field
                    class="mt-10"
                    label="Username"
                    v-model="username"
                    :rules="[rules.required]"
                ></v-text-field>

                <!-- Password -->
                <v-text-field
                    class="my-2"
                    label="Password"
                    v-model="password"
                    type="password"
                    :rules="[rules.required]"
                ></v-text-field>
                <v-btn @click="login()" color="dark-green" class="mb-8">Log me in</v-btn>
              </v-form>
            </v-card>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import Config from "@/config";
import {mapStores} from "pinia";
import {useUserStore} from "@/store/UserStore";

export default {
  name: 'LoginView',

  data() {
    return {
      username: '',
      password: '',
      formValid: true,
      rules: {
        required: value => !!value || 'Required.',
      },
    }
  },

  computed: {
    ...mapStores(useUserStore),
  },

  methods: {
    login() {
      if (this.username === Config.username && this.password === Config.password) {
        this.userStore.login();
        this.$router.push({name: 'measurement-list'});
      } else {
        alert("Invalid credentials");
      }
    },
  }
};
</script>

<style>
.fullscreen-image {
  background-image: url('@/assets/loading_image.png');
  background-position: center;
  background-size: cover;
  height: 100vh;
  opacity: 90%;
}

.landing_page_title {
  font-family: "Outfit", sans-serif;
  font-size: 90px;
  text-transform: capitalize;
  color: #FAFFF3;
  font-weight: bold;
  letter-spacing: 2px;
  text-shadow: 2px 2px 2px #323232;
}
</style>
