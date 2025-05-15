<template>
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title class="headline">{{ title }}</v-card-title>
        <v-card-text>{{ message }}</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" text @click="close">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  export default {
    name: "ErrorDialog",
    props: {
      title: {
        type: String,
        default: "Error",
      },
      message: {
        type: String,
        required: true,
      },
      modelValue: {           
        type: Boolean,
        default: false,
      },
    },
    computed: {
      dialog: {
        get() {
          return this.modelValue;
        },
        set(val) {
          this.$emit("update:modelValue", val);
        },
      },
    },
    methods: {
      close() {
        this.$emit("update:modelValue", false);
        this.$emit("close");
      },
    },
  };
  </script>
  