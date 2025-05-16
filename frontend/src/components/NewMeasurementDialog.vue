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

        <!-- Set Sensor Settings Button -->
        <v-row justify="center" class="mb-4 px-4">
          <v-btn @click="dialogSensorSettings = true" color="primary" rounded="xl" class="bg-dark-green mb-2">
            Set Sensor Settings
          </v-btn>
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
        <v-row justify="center" class="mb-4 px-4">
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
          <v-btn @click="dialogSensorSettings = true" color="primary" rounded="xl" class="bg-dark-green mb-2">
            Set Sensor Settings
          </v-btn>
        </v-row>

        <!-- Start Button -->
        <v-row justify="center" class="mb-4 px-4">
          <v-btn color="dark-green" rounded="xl" class="my-4" style="width: 300px" @click="startOneTimeMeasurement">
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
        <!-- RGB Camera Settings -->
        <v-text-field v-model="sensorSettings.rgb_image_quality" label="RGB Image Quality" type="number" min="1" max="100" />
        <v-text-field v-model="sensorSettings.rgb_image_count" label="RGB Image Count" type="number" min="1" />
        <v-text-field v-model="sensorSettings.rgb_image_width" label="RGB Image Width" type="number" min="1" />
        <v-text-field v-model="sensorSettings.rgb_image_height" label="RGB Image Height" type="number" min="1" />
        <v-text-field v-model="sensorSettings.rgb_sampling_delay" label="RGB Sampling Delay (sec)" type="number" min="0" />

        <!-- Multi-Spectral Camera Settings -->
        <v-text-field v-model="sensorSettings.ms_image_count" label="MS Image Count" type="number" min="1" />
        <v-text-field v-model="sensorSettings.ms_image_width" label="MS Image Width" type="number" min="1" />
        <v-text-field v-model="sensorSettings.ms_image_height" label="MS Image Height" type="number" min="1" />
        <v-text-field v-model="sensorSettings.ms_sampling_delay" label="MS Sampling Delay (sec)" type="number" min="0" />
        <v-text-field v-model="sensorSettings.ms_exposure_time" label="MS Exposure Time (ms)" type="number" min="0" />

        <!-- Acoustic Emission Settings -->
        <v-text-field v-model="sensorSettings.ae_voltage_format" label="AE Voltage Format" type="number" />
        <v-text-field v-model="sensorSettings.ae_voltage_dbae" label="AE Voltage DBAE" type="number" />
        <v-text-field v-model="sensorSettings.ae_counts_log" label="AE Counts Log" type="number" />
        <v-text-field v-model="sensorSettings.ae_counts_lin" label="AE Counts Lin" type="number" />
        <v-text-field v-model="sensorSettings.ae_energy_format" label="AE Energy Format" type="number" />
      </v-card-text>

      <v-card-actions>
        <v-btn text @click="dialogSensorSettings = false">Cancel</v-btn>
        <v-btn color="primary" @click="saveSensorSettings">Save</v-btn>
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
      showAlert: false,
      errorMessage: '',
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
      // Validate all required fields
      if (!this.selectedDateFrom || !this.selectedTimeFrom || !this.periodValue || !this.periodUnit || !this.aeDeltaValue || !this.aeDeltaUnit || !this.measurementName) {
        this.showAlert = true;
        this.errorMessage = 'Please fill in all required fields.';
        return;
      }

      // Set plan_from time
      const planFrom = new Date(this.selectedDateFrom);
      const [hoursFrom, minutesFrom] = this.selectedTimeFrom.split(':');
      planFrom.setHours(parseInt(hoursFrom));
      planFrom.setMinutes(parseInt(minutesFrom));
      planFrom.setSeconds(0);
      planFrom.setMilliseconds(0);

      // Check for conflicting measurements
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

      // Convert ae_delta to valid time duration format
      let aeDelta;
      if (this.aeDeltaUnit === 'Days') {
        aeDelta = `P${this.aeDeltaValue}DT0H0M`;  // Example: 1 Day = P1DT0H0M
      } else if (this.aeDeltaUnit === 'Hours') {
        aeDelta = `PT${this.aeDeltaValue}H`;  // Example: 1 Hour = PT1H
      } else if (this.aeDeltaUnit === 'Minutes') {
        aeDelta = `PT${this.aeDeltaValue}M`;  // Example: 1 Minute = PT1M
      } else if (this.aeDeltaUnit === 'Seconds') {
        aeDelta = `PT${this.aeDeltaValue}S`;  // Example: 1 Second = PT1S
      }

      // Set plan_to time if specified
      const planTo = this.selectedDateTo ? new Date(this.selectedDateTo) : planFrom;
      if (this.selectedDateTo) {
        const [hoursTo, minutesTo] = this.selectedTimeTo.split(':');
        planTo.setHours(parseInt(hoursTo));
        planTo.setMinutes(parseInt(minutesTo));
        planTo.setSeconds(0);
        planTo.setMilliseconds(0);
      }

      // Check that plan_from is earlier than plan_to
      if (planFrom >= planTo) {
        this.showAlert = true;
        this.errorMessage = 'The "From" date and time must be earlier than the "To" date and time.';
        return;
      }

      // Calculate the time differences and repetitions
      const timeDiff = planTo - planFrom;
      const periodDuration = this.convertToDuration(`PT${this.periodValue}${this.periodUnit.charAt(0)}`);
      const maxAllowedPeriods = Math.floor(timeDiff / periodDuration);

      if (this.periodValue > maxAllowedPeriods) {
        this.showAlert = true;
        this.errorMessage = `The number of repetitions exceeds the time frame. You can schedule a maximum of ${maxAllowedPeriods} repetitions.`;
        return;
      }

      // Prepare the data transfer object (DTO)
      const periodValue = this.periodValue;
      const periodUnit = this.periodUnit.charAt(0).toUpperCase();

      const dto = {
        name: this.measurementName,
        description: this.measurementDescription,
        plan_from: planFrom.toISOString(),
        plan_to: planTo.toISOString(),
        period: `P${periodValue}${periodUnit}`,
        ae_delta: aeDelta,
      };

      try {
        const response = await axios.post(`${Config.backendUrl}/measurement/periodic`, dto);
        console.log('Periodic measurements created successfully:', response.data);
        this.dialog = false;
      } catch (error) {
        this.showAlert = true;
        this.errorMessage = 'Error creating periodic measurement!';
        console.error('Error:', error);
      }
    },


    // Funkce pro kontrolu konfliktů s existujícím měřením
    async checkForConflictingMeasurements(planFrom) {
      try {
        const response = await axios.get(`${Config.backendUrl}/measurement/conflict`, {
          params: {
            planFrom: planFrom.toISOString(), // Posíláme naplánovaný čas na backend
          },
        });

        return response.data.conflict;  // Pokud existuje konflikt, vrací true
      } catch (error) {
        console.error('Error checking for conflicts:', error);
        return false;  // Pokud dojde k chybě, považujeme to za neexistenci konfliktu
      }
    },

    async startOneTimeMeasurement() {
      // Zkontrolujte, zda jsou všechny povinné hodnoty vyplněny
      if (!this.measurementName || !this.aeDeltaValue || !this.aeDeltaUnit) {
        this.showAlert = true;
        this.errorMessage = 'Please fill in all required fields.';
        return;
      }

      // Nastavení data a času pro "plan_at"
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

      // Kontrola, zda naplánovaný čas není v minulosti
      const now = new Date();
      if (planAt && planAt <= now) {
        this.showAlert = true;
        this.errorMessage = 'The planned measurement time cannot be in the past.';
        return;
      }

      // Kontrola, zda naplánovaný čas není příliš brzy s ohledem na ae_delta
      const aeDeltaDuration = this.convertToDuration(`PT${this.aeDeltaValue}${this.aeDeltaUnit.charAt(0)}`);
      if (planAt && planAt <= now.getTime() + aeDeltaDuration) {
        this.showAlert = true;
        this.errorMessage = `The planned measurement time is too soon, considering the AE delta of ${this.aeDeltaValue} ${this.aeDeltaUnit}.`;
        return;
      }

      // Odeslání požadavku na backend pro vytvoření měření
      const aeDelta = `PT${this.aeDeltaValue}${this.aeDeltaUnit.charAt(0)}`;
      const dto = {
        name: this.measurementName,
        description: this.measurementDescription,
        plan_at: planAt ? planAt.toISOString() : null,
        ae_delta: aeDelta,
        status: planAt ? 'PLANNED' : 'NEW',
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


    // Pomocná funkce pro převod ae_delta na milisekundy
    convertToDuration(aeDelta) {
      const duration = aeDelta.match(/PT(\d+)([A-Za-z]+)/);
      const value = parseInt(duration[1]);
      const unit = duration[2].toLowerCase();

      switch (unit) {
        case 'seconds': return value * 1000;
        case 'minutes': return value * 60 * 1000;
        case 'hours': return value * 60 * 60 * 1000;
        case 'days': return value * 24 * 60 * 60 * 1000;
        default: return 0;
      }
    },

    saveSensorSettings() {
      console.log('Sensor settings saved:', this.sensorSettings);
      this.dialogSensorSettings = false;
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

.v-card {
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
.v-card-actions {
  margin-top: 20px; 
  align-self: center;
}

.v-dialog {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  max-height: 80vh; /* Omezíme výšku dialogu */
}

.v-btn {
  width: 300px; /* Zajistíme, že tlačítko bude mít vždy stejnou šířku */
}


</style>