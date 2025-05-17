<template>
  <v-container fluid fill-height class="ma-0 pa-0">
    <div class="fullscreen-image pt-16">
      <v-row align="center" justify="center" fill-height class="mt-20">
        <v-col cols="6" style="height: 100%;">
          <!-- levý prázdný sloupec -->
        </v-col>

        <v-col cols="6" style="height: 100%;">
          <div class="landing_page_title">
            <span>SOAD</span><br />
            <span class="pl-8">System</span>
          </div>

          <div align="center" class="mt-10 mr-16" style="height: calc(100% - 80px);">
            <v-card class="mx-auto my-8 translucent-card" variant="tonal" rounded="xl" elevation="12"
              style="display: flex; flex-direction: column; height: 100%; max-height: 600px; width: 420px;">
              
              <v-form v-model="formValid" lazy-validation ref="form" class="pa-6" style="flex: 1; display: flex; flex-direction: column;">
                <v-text-field
                  label="Username"
                  v-model="username"
                  :rules="[rules.required]"
                  outlined
                  dense
                  color="white"
                  class="mb-4"
                ></v-text-field>

                <v-text-field
                  label="Password"
                  v-model="password"
                  type="password"
                  :rules="[rules.required]"
                  outlined
                  dense
                  color="white"
                  class="mb-6"
                ></v-text-field>

                <v-spacer></v-spacer>

                <v-btn @click="login()" color="dark-green" block>Log me in</v-btn>
              </v-form>
            </v-card>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import { mapStores } from "pinia";
import { useUserStore } from "@/store/UserStore";

export default {
  name: "LoginView",

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
  // async login(){
  //   await this.$refs.form.validate();
  //   if (!this.formValid) return;

  //   await useUserStore().login(this.username, this.password)

  //   if (!useUserStore().error) {
  //     this.$router.push(useUserStore().afterLoginRoute ?? {name: 'home'})
  //     useUserStore().setAfterLoginRoute(null)
  //   }
  // }
  login() {
      
      // this.$refs.form.validate();
      // if (!this.formValid) return;

      const envUsername = import.meta.env.VITE_ADMIN_USERNAME;
      const envPassword = import.meta.env.VITE_ADMIN_PASSWORD;
      console.log(envPassword, envUsername)
      console.log(this.username, this.password)
      if (this.username === envUsername && this.password === envPassword) {
        this.userStore.login();
        this.$router.push({ name: 'home' });
      } else {
        alert("Invalid credentials");
      }
    },
  }
}
</script>


<style scoped>
.fullscreen-image {
  position: relative;
  height: 100vh;
  background-image: url('@/assets/loading_image.png');
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

/* Přidání tmavého overlay přes pozadí */
.fullscreen-image::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 0;
}

/* Obsah nad overlay */
.v-row, .v-col, .landing_page_title, .v-card, .v-form {
  position: relative;
  z-index: 1;
}

/* Nadpis */
.landing_page_title {
  font-size: 3rem;
  font-weight: bold;
  color: white;
}

/* Malý padding vlevo u druhého řádku nadpisu */
.pl-8 {
  padding-left: 0.5rem;
}

/* Průhledná šedá karta */
.translucent-card {
  background-color: rgba(50, 50, 50, 0.7) !important;
  color: white;
}
</style>
