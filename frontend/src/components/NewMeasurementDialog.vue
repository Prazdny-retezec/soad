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
        <v-row justify="center" class="mb-4 px-4">
          <v-col cols="6">
            <v-time-picker v-model="selectedTimeFrom" format="24hr" scrollable class="w-100" />
          </v-col>
          <v-col cols="6">
            <v-date-picker v-model="selectedDateFrom" class="w-100" />
          </v-col>
        </v-row>

        <!-- Date and Time Picker (plan_to) -->
        <v-row justify="center" class="mb-4 px-4">
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
            v-model="aeDeltaValue"
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
            v-model="periodValue"
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

        <!-- Error Alert -->
        <v-row justify="center" class="mb-2 px-4">
          <v-alert
            max-width="80%"
            v-model="showAlert"
            closable
            title="Please fill in all required fields!"
            type="error"
            variant="tonal"
          ></v-alert>
        </v-row>

        <!-- Schedule Button -->
        <v-card-actions class="justify-center">
          <v-btn 
            @click="schedulePeriodicMeasurement" 
            :disabled="isLoading" 
            color="white" 
            rounded="xl" 
            class="bg-dark-green mb-2" 
            style="width: 300px"
          >
            Schedule measurement
          </v-btn>
        </v-card-actions>
      </v-card>

      <!-- ONE-TIME MEASUREMENT -->
      <v-card v-else title="Start one-time measurement" rounded="xl" class="px-4">
        <!-- Measurement Name -->
        <v-row justify="center" class="mb-4 px-4">
          <v-text-field
            v-model="measurementName"
            label="Measurement Name"
            variant="outlined"
            class="w-100"
          />
        </v-row>

        <!-- Description -->
        <v-row justify="center" class="mb-4 px-4">
          <v-textarea
            v-model="measurementDescription"
            label="Description"
            variant="outlined"
            auto-grow
            class="w-100"
          />
        </v-row>

        <!-- Date & Time -->
        <v-row justify="center" class="mb-4 px-4">
          <v-col cols="6">
            <v-time-picker v-model="selectedTime" format="24hr" scrollable class="w-100" />
          </v-col>
          <v-col cols="6">
            <v-date-picker v-model="selectedDate" class="w-100" />
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

        <!-- Start Button -->
        <v-row justify="center" class="mb-4 px-4">
          <v-btn
            color="dark-green"
            rounded="xl"
            class="my-4"
            style="width: 300px"
            @click="startOneTimeMeasurement"
          >
            Start measurement
          </v-btn>
        </v-row>

        <!-- Alert -->
        <v-row justify="center" class="my-2 px-4">
          <v-alert
            max-width="80%"
            v-model="showAlert"
            closable
            :title="errorMessage"
            type="error"
            variant="tonal"
          ></v-alert>
        </v-row>
      </v-card>
    </template>
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
    dialog: false, // Proměnná pro otevření/zavření dialogu
    selectedDateFrom: null,
    selectedTimeFrom: null,
    selectedDateTo: null,
    selectedTimeTo: null,
    aeDeltaValue: 3,
    aeDeltaUnit: 'Minutes',
    periodValue: 3,
    periodUnit: 'Days',
    measurementName: '',
    measurementDescription: '',
    showAlert: false,
    errorMessage: 'Invalid measurement setup!',
    rules: {
      required: (value) => !!value || 'Required.',
    },
  };
},


  setup() {
    const measurementStore = useMeasurementStore();
    return {
      measurementStore,
    };
  },
  methods: {
    async schedulePeriodicMeasurement() {
      if (!this.selectedDateFrom || !this.selectedTimeFrom || !this.periodValue || !this.periodUnit || !this.aeDeltaValue || !this.aeDeltaUnit || !this.measurementName) {
        this.showAlert = true;
        this.errorMessage = 'Please fill in all required fields.';
        return;
      }

      const planFrom = new Date(this.selectedDateFrom);
      const [hours, minutes] = this.selectedTimeFrom.split(':');
      planFrom.setHours(parseInt(hours));
      planFrom.setMinutes(parseInt(minutes));
      planFrom.setSeconds(0);
      planFrom.setMilliseconds(0);

      const aeDelta = `PT${this.aeDeltaValue}${this.aeDeltaUnit.charAt(0)}`; // AE Delta in ISO 8601 format
      const periodValue = this.periodValue;
      const periodUnit = this.periodUnit.charAt(0).toUpperCase(); // First character (e.g., 'D' for Days)

      const dto = {
        name: this.measurementName,
        description: this.measurementDescription,
        plan_from: planFrom.toISOString(), // plan_from in ISO format
        plan_to: this.selectedDateTo ? new Date(this.selectedDateTo).toISOString() : planFrom.toISOString(),
        period: `P${periodValue}${periodUnit}`, // Period in ISO 8601 format
        ae_delta: aeDelta, // AE delta in the correct format
      };

      try {
        const measurementStore = useMeasurementStore();
        const response = await measurementStore.createPeriodicMeasurement(dto);
        console.log('Periodic measurements created successfully:', response);
        this.dialog = false; // Close the dialog after successful submission
      } catch (error) {
        this.showAlert = true;
        this.errorMessage = 'Error creating periodic measurement!';
        console.error('Error:', error);
      }
    },

    async startOneTimeMeasurement() {
      if (!this.measurementName || !this.aeDeltaValue || !this.aeDeltaUnit) {
        this.showAlert = true;
        this.errorMessage = 'Please fill in all required fields.';
        return;
      }

      const status = this.selectedDate && this.selectedTime ? 'PLANNED' : 'NEW';

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

      const aeDelta = `PT${this.aeDeltaValue}${this.aeDeltaUnit.charAt(0)}`;

      const dto = {
        name: this.measurementName,
        description: this.measurementDescription,
        plan_at: planAt ? planAt.toISOString() : null,
        ae_delta: aeDelta,
        status,
      };

      try {
        const response = await axios.post(`${Config.backendUrl}/measurement`, dto);
        console.log('Measurement created successfully:', response.data);
        this.dialog = false;
      } catch (error) {
        this.showAlert = true;
        this.errorMessage = 'Error creating measurement!';
        console.error('Error:', error);
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
    },
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
}
</style>
