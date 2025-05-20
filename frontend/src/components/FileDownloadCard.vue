<template>
  <v-card class="file-card" outlined>
    <v-card-title class="d-flex align-center">
      <v-icon class="mr-3" color="green">mdi-file-download</v-icon>
      <div class="text-truncate">
        <div class="font-weight-medium">{{ props.filename }}</div>
        <div class="text-caption text-grey">Click for download</div>
      </div>
      <v-spacer/>
      <v-btn :href="url" icon variant="text" download :title="`Download ${props.filename}`">
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-card-title>
  </v-card>
</template>

<script setup>

const props = defineProps({
  filename: {
    type: String,
    required: true
  },
  url: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.file-card {
  transition: box-shadow 0.3s ease;
}

.file-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.text-truncate {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>