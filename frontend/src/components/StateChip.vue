<script setup>
import { computed } from 'vue';

const props = defineProps({
  state: {
    type: String,
    required: true,
  },
});

const color = computed(() => {
  switch (props.state) {
    case 'NEW':
      return 'blue';
    case 'PLANNED':
      return 'deep-purple';
    case 'DOWNLOADING':
      return 'indigo';
    case 'ZIPPING':
      return 'orange';
    case 'UPLOADING':
      return 'teal';
    case 'ERROR':
      return 'red';
    case 'FINISHED':
      return 'green';
    case 'CANCELLED':
      return 'grey';
    default:
      return 'grey';
  }
});

const label = computed(() => {
  return props.state.charAt(0) + props.state.slice(1).toLowerCase();
});
</script>

<template>
  <v-chip
    class="ma-1"
    :color="color"
    text-color="white"
    size="small"
    label
  >
    <v-icon start size="10" class="mr-1">mdi-circle</v-icon>
    {{ label }}
  </v-chip>
</template>

<style scoped>

</style>