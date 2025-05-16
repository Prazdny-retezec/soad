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

          <!-- Display Sensor Settings -->
          <v-list-item title="RGB Image Quality" :subtitle="detail.sensor_settings.rgb_image_quality"></v-list-item>
          <v-list-item title="RGB Image Count" :subtitle="detail.sensor_settings.rgb_image_count"></v-list-item>
          <v-list-item title="RGB Image Width" :subtitle="detail.sensor_settings.rgb_image_width"></v-list-item>
          <v-list-item title="RGB Image Height" :subtitle="detail.sensor_settings.rgb_image_height"></v-list-item>
          <v-list-item title="RGB Sampling Delay" :subtitle="detail.sensor_settings.rgb_sampling_delay"></v-list-item>
          <v-list-item title="MS Image Count" :subtitle="detail.sensor_settings.ms_image_count"></v-list-item>
          <v-list-item title="MS Image Width" :subtitle="detail.sensor_settings.ms_image_width"></v-list-item>
          <v-list-item title="MS Image Height" :subtitle="detail.sensor_settings.ms_image_height"></v-list-item>
          <v-list-item title="MS Sampling Delay" :subtitle="detail.sensor_settings.ms_sampling_delay"></v-list-item>
          <v-list-item title="MS Exposure Time" :subtitle="detail.sensor_settings.ms_exposure_time"></v-list-item>
          <v-list-item title="AE Voltage Format" :subtitle="detail.sensor_settings.ae_voltage_format"></v-list-item>
          <v-list-item title="AE Voltage DBAE" :subtitle="detail.sensor_settings.ae_voltage_dbae"></v-list-item>
          <v-list-item title="AE Counts Log" :subtitle="detail.sensor_settings.ae_counts_log"></v-list-item>
          <v-list-item title="AE Counts Lin" :subtitle="detail.sensor_settings.ae_counts_lin"></v-list-item>
          <v-list-item title="AE Energy Format" :subtitle="detail.sensor_settings.ae_energy_format"></v-list-item>
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

          <!-- SENSOR SETTINGS IN EDIT MODE -->
          <v-divider class="my-4"></v-divider>
          <v-card-title class="text-h5">Sensor Settings</v-card-title>

          <!-- RGB Image Settings -->
          <v-text-field 
            v-model="editedSensorSettings.rgb_image_quality" 
            label="RGB Image Quality" 
            type="number" 
            min="1" 
            max="100" 
          />
          <v-text-field 
            v-model="editedSensorSettings.rgb_image_count" 
            label="RGB Image Count" 
            type="number" 
            min="1" 
          />
          <v-text-field 
            v-model="editedSensorSettings.rgb_image_width" 
            label="RGB Image Width" 
            type="number" 
            min="1" 
          />
          <v-text-field 
            v-model="editedSensorSettings.rgb_image_height" 
            label="RGB Image Height" 
            type="number" 
            min="1" 
          />
          <v-text-field 
            v-model="editedSensorSettings.rgb_sampling_delay" 
            label="RGB Sampling Delay (sec)" 
            type="number" 
            min="0" 
          />

          <!-- MS Image Settings -->
          <v-text-field 
            v-model="editedSensorSettings.ms_image_count" 
            label="MS Image Count" 
            type="number" 
            min="1" 
          />
          <v-text-field 
            v-model="editedSensorSettings.ms_image_width" 
            label="MS Image Width" 
            type="number" 
            min="1" 
          />
          <v-text-field 
            v-model="editedSensorSettings.ms_image_height" 
            label="MS Image Height" 
            type="number" 
            min="1" 
          />
          <v-text-field 
            v-model="editedSensorSettings.ms_sampling_delay" 
            label="MS Sampling Delay (sec)" 
            type="number" 
            min="0" 
          />
          <v-text-field 
            v-model="editedSensorSettings.ms_exposure_time" 
            label="MS Exposure Time (ms)" 
            type="number" 
            min="0" 
          />

          <!-- AE Image Settings -->
          <v-text-field 
            v-model="editedSensorSettings.ae_voltage_format" 
            label="AE Voltage Format" 
            type="number" 
          />
          <v-text-field 
            v-model="editedSensorSettings.ae_voltage_dbae" 
            label="AE Voltage DBAE" 
            type="number" 
          />
          <v-text-field 
            v-model="editedSensorSettings.ae_counts_log" 
            label="AE Counts Log" 
            type="number" 
          />
          <v-text-field 
            v-model="editedSensorSettings.ae_counts_lin" 
            label="AE Counts Lin" 
            type="number" 
          />
          <v-text-field 
            v-model="editedSensorSettings.ae_energy_format" 
            label="AE Energy Format" 
            type="number" 
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

          <v-btn
            class="mr-2 mb-2"
            variant="tonal"
            color="secondary"
            v-if="detail.state === 'PLANNED'"
            @click="unplanMeasurement(detail.id)"
          >
            Unplan
          </v-btn>
          <v-btn
            class="mr-2 mb-2"
            variant="tonal"
            color="primary"
            v-if="detail.state === 'NEW'"
            @click="openPlanDialog"
          >
            Plan
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import { useMeasurementStore } from '@/store/MeasurementStore';
import axios from 'axios';
import Config from '@/config';

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
      editedSensorSettings: {},
      planDialog: false,
      selectedDateFrom: null,
      selectedTimeFrom: null,
      aeDeltaValue: 3,
      aeDeltaUnit: 'Days',
    };
  },
  async created() {
    const measurementStore = useMeasurementStore();
    this.detail = await measurementStore.getMeasurement(this.measurementId);
    if (this.detail.sensor_settings) {
      this.editedSensorSettings = { ...this.detail.sensor_settings };
    }
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
      this.editedSensorSettings = { ...this.detail.sensor_settings };
    },
    cancelEditing() {
      this.isEditing = false;
      this.editedName = '';
      this.editedDescription = '';
      this.editedSensorSettings = {}; // Reset sensor settings
    },

    async submitUpdate() {
      const dto = {
        name: this.editedName,
        description: this.editedDescription,
        sensor_settings: this.editedSensorSettings, // Include sensor settings in the update
      };

      try {
        const measurementStore = useMeasurementStore();
        await measurementStore.updateMeasurement(this.detail.id, dto); // Update with sensor settings
        this.detail = await measurementStore.getMeasurement(this.detail.id); // Refresh detail
        this.isEditing = false;
        alert('Measurement updated successfully.');
      } catch (error) {
        console.error('Error:', error);
        alert('Error updating measurement.');
      }
    },

    openPlanDialog() {
      this.planDialog = true;
    },

    async submitPlan() {
      if (!this.selectedDateFrom || !this.selectedTimeFrom) {
        alert('Please select both date and time.');
        return;
      }

      const planDate = new Date(this.selectedDateFrom);
      const [hours, minutes] = this.selectedTimeFrom.split(':');
      planDate.setHours(parseInt(hours));
      planDate.setMinutes(parseInt(minutes));
      planDate.setSeconds(0);

      let aeDeltaPrefix = 'P';
      const aeDeltaUnitChar = this.aeDeltaUnit.charAt(0);
      if (['H', 'M', 'S'].includes(aeDeltaUnitChar)) aeDeltaPrefix = 'PT';

      const dto = {
        plan_at: planDate.toISOString(),
        ae_delta: `${aeDeltaPrefix}${this.aeDeltaValue}${aeDeltaUnitChar}`,
      };

      try {
        const measurementStore = useMeasurementStore();
        await measurementStore.planMeasurement(this.detail.id, dto.plan_at, dto.ae_delta);
        this.detail = await measurementStore.getMeasurement(this.detail.id);
        this.planDialog = false;
        alert('Measurement successfully planned.');
      } catch (error) {
        console.error('Error:', error);
        alert('Error planning measurement.');
      }
    },

    async unplanMeasurement(id) {
      const measurementStore = useMeasurementStore();
      await measurementStore.unplanMeasurement(id);
      this.detail.state = 'NEW';  // Change state to NEW after unplanning
      this.detail.planned_at = null; // Remove planned_at
    },
  },
};
</script>

<style scoped>
.v-text-field,
.v-textarea {
  max-width: 100%;
  margin: 0 auto;
}
</style>
