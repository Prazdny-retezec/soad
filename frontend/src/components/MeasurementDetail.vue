<template>
  <v-dialog max-width="500" v-model="dialog">
    <template v-slot:activator="{ props: activatorProps }">
      <v-icon v-bind="activatorProps" size="20">mdi-eye-outline</v-icon>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card rounded="xl">
        <v-row justify="space-between" class="align-center">
          <v-col class="pr-4" cols="auto">
            <v-card-title class="text-h5">Measurement Information</v-card-title>
          </v-col>
          <v-col class="pr-6" cols="auto">
            <v-icon @click="closeDialog(isActive)" size="30">mdi-close</v-icon>
          </v-col>
        </v-row>

        <!-- DISPLAY MODE -->
        <v-list lines="two" class="ml-2" v-if="detail && !isEditing">
          <v-list-item title="Name" :subtitle="detail.name"></v-list-item>
          <v-list-item title="Description" :subtitle="detail.description"></v-list-item>
          <v-list-item title="Created At" :subtitle="formatDate(detail.created_at)"></v-list-item>
          <v-list-item title="Updated At" :subtitle="formatDate(detail.updated_at)"></v-list-item>
          <v-list-item title="Planned At" :subtitle="formatDate(detail.planned_at)"></v-list-item>
          <v-list-item v-if="detail.started_at" title="Started At" :subtitle="formatDate(detail.started_at)"></v-list-item>
          <v-list-item v-if="detail.ended_at" title="Ended At" :subtitle="formatDate(detail.ended_at)"></v-list-item>
          <v-list-item title="State" :subtitle="detail.state"></v-list-item>
          <v-list-item v-if="detail.result" title="Result" :subtitle="detail.result"></v-list-item>
        </v-list>

        <!-- EDIT MODE -->
        <v-container v-if="detail && isEditing">
          <v-text-field
            v-model="editedName"
            label="Measurement Name"
            variant="outlined"
            class="mb-3"
          />
          <v-textarea
            v-model="editedDescription"
            label="Description"
            variant="outlined"
            auto-grow
          />
        </v-container>

        <!-- ACTION BUTTONS -->
        <v-card-actions v-if="detail">
          <v-spacer></v-spacer>

          <v-btn
            class="mr-2 mb-2"
            variant="tonal"
            color="dark-green"
            v-if="!isEditing"
            :disabled="detail.state === 'PLANNED' || detail.state === 'CANCELLED'"
            @click="handleDownload(detail.id); isActive.value = false"
          >
            Download
          </v-btn>

          <v-btn
            class="mr-2 mb-2"
            variant="outlined"
            color="primary"
            v-if="!isEditing"
            @click="startEditing"
          >
            Edit
          </v-btn>

          <v-btn
            class="mr-2 mb-2"
            variant="tonal"
            color="dark-green"
            v-if="isEditing"
            @click="submitUpdate"
          >
            Save
          </v-btn>

          <v-btn
            class="mr-2 mb-2"
            variant="text"
            color="red"
            v-if="isEditing"
            @click="cancelEditing"
          >
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import Config from '@/config';
import { useMeasurementStore } from '@/store/MeasurementStore';

export default {
  name: 'MeasurementDetail',
  props: {
    measurementId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      detail: null,
      dialog: false,
      isEditing: false,
      editedName: '',
      editedDescription: '',
    };
  },
  async created() {
    const measurementStore = useMeasurementStore();
    this.detail = await measurementStore.getMeasurement(this.measurementId);
  },
  methods: {
    formatDate(dateString) {
      return dateString ? new Date(dateString).toLocaleString() : 'N/A';
    },
    handleDownload(id) {
      const link = Config.backendUrl + `/measurement/${id}/download`;
      window.open(link);
    },
    closeDialog(isActive) {
      isActive.value = false;
    },
    startEditing() {
      this.editedName = this.detail.name;
      this.editedDescription = this.detail.description;
      this.isEditing = true;
    },
    cancelEditing() {
      this.isEditing = false;
      this.editedName = '';
      this.editedDescription = '';
    },
    async submitUpdate() {
      const measurementStore = useMeasurementStore();
      const dto = {
        name: this.editedName,
        description: this.editedDescription,
      };

      const updated = await measurementStore.updateMeasurement(this.detail.id, dto);

      if (!measurementStore.error) {
        this.detail = updated; // Full refresh of local detail
        this.isEditing = false;
      } else {
        alert(measurementStore.error);
      }
    },
  },
};
</script>

<style scoped>
.v-text-field,
.v-textarea {
  max-width: 90%;
  margin: 0 auto;
}
</style>
