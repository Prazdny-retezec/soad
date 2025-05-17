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
import Config from "@/config";
import { mapStores } from "pinia";
import { useUserStore } from "@/store/UserStore";

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
        this.$router.push({ name: 'measurement-list' });
      } else {
        alert("Invalid credentials");
      }
    },
  }
};
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

.v-row, .v-col, .landing_page_title, .v-card, .v-form {
  position: relative;
  z-index: 1;
}

/* Nadpis */
.landing_page_title {
  font-family: "Outfit", sans-serif;
  font-size: 90px;
  text-transform: capitalize;
  color: #FAFFF3;
  font-weight: bold;
  letter-spacing: 2px;
  text-shadow: 2px 2px 2px #323232;
}

/* Malý padding vlevo u druhého řádku nadpisu */
.pl-8 {
  padding-left: 0.5rem;
}

/* Průhledná šedá karta - méně světlá, více průhledná */
.translucent-card {
  background-color: rgba(200, 200, 200, 0.15) !important; /* méně intenzivní než předtím */
  color: #f0f0f0;
}

.v-input input {
  background-color: rgba(255, 255, 255, 0.2) !important;
  color: #fff !important; /* čistě bílý text */
  caret-color: #fff !important; /* bílý kurzor */
  border-radius: 4px;
  padding-left: 8px;
}

/* Labely světlejší a výraznější */
.v-input .v-label {
  color: #eee !important;
  font-weight: 500;
}

/* Placeholder text světlejší */
.v-input input::placeholder {
  color: #ddd !important;
  opacity: 1;
}

/* Rámeček vstupních polí */
.v-input.v-input--is-focused .v-input__control {
  border-color: #80d8ff !important; /* světle modrý rámeček při focusu */
  box-shadow: 0 0 5px #80d8ff !important;
}

.v-input:not(.v-input--is-focused) .v-input__control {
  border-color: #ccc !important; /* světle šedý rámeček */
}

</style>
