<template>
  <v-dialog max-width="700" v-model="dialog">
    <template v-slot:activator="{ props: activatorProps }">
      <div v-bind="activatorProps">
        <span v-if="type === 'schedule'">Periodic Schedule</span>
        <span v-else>One time measurement</span>
      </div>
    </template>

    <template v-slot:default="{ isActive }">
      <!-- PERIODIC SCHEDULING -->
      <v-card v-if="type === 'schedule'" title="Schedule measurement" rounded="xl" class="px-4">
        <!-- Measurement Name -->
        <v-row justify="center" class="mb-4 px-4">
          <v-text-field
            v-model="measurementName"
            label="Measurement Name"
            variant="outlined"
            :rules="[rules.required]"
            class="w-100"
          />
        </v-row>

        <!-- Measurement Description -->
        <v-row justify="center" class="mb-4 px-4">
          <v-textarea
            v-model="measurementDescription"
            label="Description"
            variant="outlined"
            auto-grow
            :rules="[rules.required]"
            class="w-100"
          />
        </v-row>

        <!-- Date and Time Picker (plan_from) -->
        <v-row justify="center">
          <v-col cols="6">
            <v-time-picker v-model="selectedTimeFrom" format="24hr" scrollable class="w-100" />
          </v-col>
          <v-col cols="6">
            <v-date-picker v-model="selectedDateFrom" class="w-100" />
          </v-col>
        </v-row>

        <!-- Date and Time Picker (plan_to) -->

        <v-row justify="center">
          <v-col cols="6">
            <v-time-picker v-model="selectedTimeTo" format="24hr" scrollable class="w-100" />
          </v-col>
          <v-col cols="6">
            <v-date-picker v-model="selectedDateTo" class="w-100" />
          </v-col>
        </v-row>

        <!-- AE Delta Selection -->
        <v-row justify="center" class="mb-4 px-4">
          <v-text-field
            v-model.number="aeDeltaValue"
            label="AE Delta Value"
            type="number"
            min="1"
            variant="outlined"
            class="mr-2"
          />
          <v-select
            v-model="aeDeltaUnit"
            label="AE Delta Unit"
            :items="['Seconds', 'Minutes', 'Hours', 'Days']"
            variant="outlined"
            class="mr-2"
          />
        </v-row>

        <!-- Period Selection -->
        <v-row justify="center" class="mb-4 px-4">
          <v-text-field
            v-model.number="periodValue"
            label="Period Value (e.g. 3)"
            type="number"
            min="1"
            variant="outlined"
            class="mr-2"
          />
          <v-select
            v-model="periodUnit"
            label="Period Unit"
            :items="['Days', 'Weeks', 'Months']"
            variant="outlined"
            class="mr-2"
          />
        </v-row>

        <!-- Set Sensor Settings Button -->
        <v-row justify="center" class="mb-4 px-4">
          <v-btn @click="openSensorSettingsDialog" color="primary" rounded="xl" class="bg-dark-green mb-2">
            Set Sensor Settings
          </v-btn>
        </v-row>

        <!-- Schedule Button -->
        <v-card-actions class="justify-center">
          <v-btn
            @click="schedulePeriodicMeasurement"
            :disabled="isLoading"
            color="black"
            rounded="xl"
            class="bg-dark-green mb-2"
          >
            Schedule measurement
          </v-btn>
        </v-card-actions>

        <!-- Error Alert -->
        <v-row justify="center" class="my-2 px-4">
          <v-alert max-width="100%" v-if="showAlert" closable :title="errorMessage" type="error" variant="tonal"></v-alert>
        </v-row>
      </v-card>

      <!-- ONE-TIME MEASUREMENT -->
      <v-card v-else title="Start one-time measurement" rounded="xl" class="px-4">
        <!-- Measurement Name -->
        <v-row justify="center" class="mb-4 px-4">
          <v-text-field v-model="measurementName" label="Measurement Name" variant="outlined" class="w-100" />
        </v-row>

        <!-- Description -->
        <v-row justify="center" class="mb-4 px-4">
          <v-textarea v-model="measurementDescription" label="Description" variant="outlined" auto-grow class="w-100" />
        </v-row>

        <!-- Date & Time -->
        <v-row justify="center">
          <v-col cols="6">
            <v-time-picker v-model="selectedTime" format="24hr" scrollable class="w-100" />
          </v-col>
          <v-col cols="6">
            <v-date-picker v-model="selectedDate" class="w-100" :max="maxDate" format="yyyy-MM-dd" />
          </v-col>
        </v-row>

        <!-- Delta -->
        <v-row justify="center" class="mb-4 px-4">
          <v-col cols="6">
            <v-text-field
              v-model.number="aeDeltaValue"
              label="Delta Value"
              type="number"
              min="1"
              variant="outlined"
            />
          </v-col>
          <v-col cols="6">
            <v-select
              v-model="aeDeltaUnit"
              label="Delta Unit"
              :items="['Seconds', 'Minutes', 'Hours', 'Days']"
              variant="outlined"
            />
          </v-col>
        </v-row>

        <!-- Set Sensor Settings Button -->
        <v-row justify="center" class="mb-4 px-4">
          <v-btn @click="openSensorSettingsDialog" color="primary" rounded="xl" class="bg-dark-green mb-2">
            Set Sensor Settings
          </v-btn>
        </v-row>

        <!-- Start Button -->
        <v-row justify="center" class="mb-4 px-4">
          <v-btn color="dark-green" rounded="xl" class="my-4" @click="startOneTimeMeasurement">
            Start measurement
          </v-btn>
        </v-row>

        <!-- Error Alert -->
        <v-row justify="center" class="my-2 px-4">
          <v-alert max-width="100%" v-if="showAlert" closable :title="errorMessage" type="error" variant="tonal"></v-alert>
        </v-row>
      </v-card>
    </template>
  </v-dialog>

  <!-- Dialog for Sensor Settings -->
  <v-dialog v-model="dialogSensorSettings" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">Sensor Settings</span>
      </v-card-title>

      <v-card-text>
        <v-text-field v-model.number="tempSensorSettings.rgb_image_quality" label="RGB Image Quality" type="number" min="1" max="100" />
        <v-text-field v-model.number="tempSensorSettings.rgb_image_count" label="RGB Image Count" type="number" min="1" />
        <v-text-field v-model.number="tempSensorSettings.rgb_image_width" label="RGB Image Width" type="number" min="1" />
        <v-text-field v-model.number="tempSensorSettings.rgb_image_height" label="RGB Image Height" type="number" min="1" />
        <v-text-field v-model.number="tempSensorSettings.rgb_sampling_delay" label="RGB Sampling Delay (sec)" type="number" min="0" />

        <v-text-field v-model.number="tempSensorSettings.ms_image_count" label="MS Image Count" type="number" min="1" />
        <v-text-field v-model.number="tempSensorSettings.ms_image_width" label="MS Image Width" type="number" min="1" />
        <v-text-field v-model.number="tempSensorSettings.ms_image_height" label="MS Image Height" type="number" min="1" />
        <v-text-field v-model.number="tempSensorSettings.ms_sampling_delay" label="MS Sampling Delay (sec)" type="number" min="0" />
        <v-text-field v-model.number="tempSensorSettings.ms_exposure_time" label="MS Exposure Time (ms)" type="number" min="0" />

        <v-text-field v-model.number="tempSensorSettings.ae_voltage_format" label="AE Voltage Format" type="number" />
        <v-text-field v-model.number="tempSensorSettings.ae_voltage_dbae" label="AE Voltage DBAE" type="number" />
        <v-text-field v-model.number="tempSensorSettings.ae_counts_log" label="AE Counts Log" type="number" />
        <v-text-field v-model.number="tempSensorSettings.ae_counts_lin" label="AE Counts Lin" type="number" />
        <v-text-field v-model.number="tempSensorSettings.ae_energy_format" label="AE Energy Format" type="number" />
      </v-card-text>

      <v-card-actions>
        <v-btn width = "35pt" class="mr-2 mb-2" variant="tonal" text @click="cancelSensorSettings">Cancel</v-btn>
        <v-btn width = "35pt" class="mr-2 mb-2" variant="tonal" color="primary" @click="saveSensorSettings">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { useMeasurementStore } from '@/store/MeasurementStore';
import axios from 'axios';
import Config from '@/config';

export default {
  name: 'NewMeasurementDialog',

  props: {
    type: String,
  },

  data() {
    return {
      dialog: false,
      dialogSensorSettings: false,
      sensorSettings: {
        rgb_image_quality: 90,
        rgb_image_count: 5,
        rgb_image_width: 1920,
        rgb_image_height: 1080,
        rgb_sampling_delay: 2,

        ms_image_count: 2,
        ms_image_width: 1920,
        ms_image_height: 1080,
        ms_sampling_delay: 5,
        ms_exposure_time: 60,

        ae_voltage_format: 5,
        ae_voltage_dbae: 1,
        ae_counts_log: 1,
        ae_counts_lin: 1,
        ae_energy_format: 1
      },
      tempSensorSettings: null, // <-- dočasná kopie pro editaci
      measurementName: '',
      measurementDescription: '',
      aeDeltaValue: 3,
      aeDeltaUnit: 'Minutes',
      periodValue: 3,
      periodUnit: 'Days',
      selectedDateFrom: null,
      selectedTimeFrom: null,
      selectedDateTo: null,
      selectedTimeTo: null,
      selectedDate: null,
      selectedTime: null,
      showAlert: false,
      errorMessage: '',
      rules: {
        required: (value) => !!value || 'Required.',
      },
      isLoading: false,
    };
  },

  setup() {
    const measurementStore = useMeasurementStore();
    return {
      measurementStore,
    };
  },

  methods: {
    openSensorSettingsDialog() {
      this.tempSensorSettings = JSON.parse(JSON.stringify(this.sensorSettings));
      this.dialogSensorSettings = true;
    },

    saveSensorSettings() {
      this.sensorSettings = JSON.parse(JSON.stringify(this.tempSensorSettings));
      this.dialogSensorSettings = false;
    },

    cancelSensorSettings() {
      this.dialogSensorSettings = false;
      this.tempSensorSettings = null;
    },

    async schedulePeriodicMeasurement() {
      if (
        !this.selectedDateFrom || !this.selectedTimeFrom || !this.periodValue || !this.periodUnit ||
        !this.aeDeltaValue || !this.aeDeltaUnit || !this.measurementName
      ) {
        this.showAlert = true;
        this.errorMessage = 'Please fill in all required fields.';
        return;
      }

      const planFrom = new Date(this.selectedDateFrom);
      const [hoursFrom, minutesFrom] = this.selectedTimeFrom.split(':');
      planFrom.setHours(parseInt(hoursFrom));
      planFrom.setMinutes(parseInt(minutesFrom));
      planFrom.setSeconds(0);
      planFrom.setMilliseconds(0);

      const conflict = await this.checkForConflictingMeasurements(planFrom);
      if (conflict) {
        this.showAlert = true;
        this.errorMessage = 'A measurement is already scheduled for the selected time.';
        return;
      }

      const now = new Date();
      if (planFrom <= now) {
        this.showAlert = true;
        this.errorMessage = 'The planned measurement time cannot be in the past.';
        return;
      }

      // Převod aeDelta na ISO8601
      let aeDelta;
      if (this.aeDeltaUnit === 'Days') {
        aeDelta = `P${this.aeDeltaValue}DT0H0M`;
      } else if (this.aeDeltaUnit === 'Hours') {
        aeDelta = `PT${this.aeDeltaValue}H`;
      } else if (this.aeDeltaUnit === 'Minutes') {
        aeDelta = `PT${this.aeDeltaValue}M`;
      } else if (this.aeDeltaUnit === 'Seconds') {
        aeDelta = `PT${this.aeDeltaValue}S`;
      }

      const planTo = this.selectedDateTo ? new Date(this.selectedDateTo) : planFrom;
      if (this.selectedDateTo) {
        const [hoursTo, minutesTo] = this.selectedTimeTo.split(':');
        planTo.setHours(parseInt(hoursTo));
        planTo.setMinutes(parseInt(minutesTo));
        planTo.setSeconds(0);
        planTo.setMilliseconds(0);
      }

      if (planFrom >= planTo) {
        this.showAlert = true;
        this.errorMessage = 'The "From" date and time must be earlier than the "To" date and time.';
        return;
      }

      const periodValue = this.periodValue;
      const periodUnit = this.periodUnit.charAt(0).toUpperCase();
      const period = `P${periodValue}${periodUnit}`;

      const dto = {
        name: this.measurementName,
        description: this.measurementDescription,
        plan_from: planFrom.toISOString(),
        plan_to: planTo.toISOString(),
        period: period,
        ae_delta: aeDelta,
        sensor_settings: this.sensorSettings,  // POZOR TADY!!
      };

      try {
        this.isLoading = true;
        const response = await axios.post(`${Config.backendUrl}/measurement/periodic`, dto);
        console.log('Periodic measurements created:', response.data);
        this.dialog = false;
        this.showAlert = false;
      } catch (error) {
        this.showAlert = true;
        this.errorMessage = 'Error creating periodic measurement!';
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },

    async startOneTimeMeasurement() {
      if (!this.measurementName || !this.aeDeltaValue || !this.aeDeltaUnit) {
        this.showAlert = true;
        this.errorMessage = 'Please fill in all required fields.';
        return;
      }

      const planAt = this.selectedDate && this.selectedTime
        ? (() => {
            const date = new Date(this.selectedDate);
            const [hours, minutes] = this.selectedTime.split(':');
            date.setHours(parseInt(hours));
            date.setMinutes(parseInt(minutes));
            date.setSeconds(0);
            date.setMilliseconds(0);
            return date;
          })()
        : null;

      const now = new Date();
      if (planAt && planAt <= now) {
        this.showAlert = true;
        this.errorMessage = 'The planned measurement time cannot be in the past.';
        return;
      }

      let aeDelta;
      if (this.aeDeltaUnit === 'Days') {
        aeDelta = `P${this.aeDeltaValue}DT0H0M`;
      } else if (this.aeDeltaUnit === 'Hours') {
        aeDelta = `PT${this.aeDeltaValue}H`;
      } else if (this.aeDeltaUnit === 'Minutes') {
        aeDelta = `PT${this.aeDeltaValue}M`;
      } else if (this.aeDeltaUnit === 'Seconds') {
        aeDelta = `PT${this.aeDeltaValue}S`;
      }

      const dto = {
        name: this.measurementName,
        description: this.measurementDescription,
        plan_at: planAt ? planAt.toISOString() : null,
        ae_delta: aeDelta,
        sensor_settings: this.sensorSettings,
      };

      try {
        this.isLoading = true;
        const response = await axios.post(`${Config.backendUrl}/measurement`, dto);
        console.log('Measurement created:', response.data);
        this.dialog = false;
        this.showAlert = false;
      } catch (error) {
        this.showAlert = true;
        this.errorMessage = 'Error creating measurement!';
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },


    closeDialog() {
      this.selectedDate = null;
      this.selectedTime = null;
      this.measurementName = '';
      this.measurementDescription = '';
      this.aeDeltaValue = 3;
      this.aeDeltaUnit = 'Minutes';
      this.dialog = false;
      this.showAlert = false;
      this.tempSensorSettings = null;
    },
  },

  async checkForConflictingMeasurements(planFrom) {
      try {
        const response = await axios.get(`${Config.backendUrl}/measurement/conflict`, {
          params: {
            planFrom: planFrom.toISOString(),
          },
        });
        return response.data.conflict;
      } catch (error) {
        console.error('Error checking for conflicts:', error);
        return false;
      }
    },
};
</script>

<style scoped>
.v-card-actions {
  height: 50px;
  margin: 1%;
}

.v-date-picker .v-date-picker-header__content {
  font-size: 22px;
}

.v-time-picker .v-time-picker-controls__time__btn.v-btn--density-default.v-btn {
  width: 74px;
  height: 63px;
  font-size: 27px;
}

.v-time-picker .v-time-picker-controls__time__separator {
  font-size: 38px;
  height: 80px;
  width: 22px;
  text-align: center;
}

.v-time-picker .v-time-picker-controls {
  margin-bottom: 10px;
}

.v-card {
  padding-left: 2rem;
  padding-right: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.v-alert {
  margin-bottom: 20px; 
  max-width: 100%; 
  padding: 20px;
  font-size: 16px;
  line-height: 1.5;
  background-color: #f8d7da; 
  color: #721c24; 
  border: 1px solid #f5c6cb; 
  border-radius: 5px; 
}

.v-btn {
  width: 300pt;
}

.v-row > .v-col.pr-2 {
  padding-right: 8px !important;
}

.v-row > .v-col.pl-2 {
  padding-left: 8px !important;
}

</style>
