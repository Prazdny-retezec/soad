<template>
  <v-dialog v-model="dialog" max-width="700" variant="outlined">
    <template v-slot:activator="{ props: activatorProps }">
      <div v-bind="activatorProps">
        <span v-if="type === 'schedule'">Periodic Schedule</span>
        <span v-else>One time measurement</span>
      </div>
    </template>

    <template v-slot:default="{ isActive }">
      <!-- PERIODIC SCHEDULING -->
      <v-card v-if="type === 'schedule'" title="Schedule measurement" rounded="xl">
        <div>
          <v-icon @click="closeDialog()" style="position: absolute; top: 20px; right: 20px">mdi mdi-close</v-icon>
        </div>

        <v-card-text class="subtitle text-dark-green">Select type of measurement</v-card-text>

        <v-row justify="center">
          <v-select
            style="max-width: 80%"
            clearable
            chips
            label="Type"
            :items="['RGB camera', 'Hyperspectral camera', 'Acoustic emission']"
            multiple
            variant="outlined"
            :rules="[rules.required]"
          ></v-select>
        </v-row>

        <v-row justify="center">
          <v-time-picker class="text-dark-green" v-model="selectedTime" format="24hr" scrollable />
          <v-date-picker v-model="selectedDate" />
        </v-row>

        <v-row justify="center" class="mb-2">
          <v-alert
            max-width="80%"
            v-model="showAlert"
            closable
            title="Please fill in the date and time!"
            type="error"
            variant="tonal"
          ></v-alert>
        </v-row>

        <v-card-actions class="justify-center">
          <v-btn @click="scheduleMeasurement()" color="white" rounded="xl" class="bg-dark-green mb-2" style="width: 300px">
            Schedule measurement
          </v-btn>
        </v-card-actions>
      </v-card>

      <!-- ONE-TIME MEASUREMENT -->
      <v-card v-else title="Start one-time measurement" rounded="xl">
        <div>
          <v-icon @click="closeDialog()" style="position: absolute; top: 20px; right: 20px">mdi mdi-close</v-icon>
        </div>

        <v-card-text class="subtitle text-dark-green">
          Select time of measurement. AE starts ± delta around the selected time.
        </v-card-text>

        <!-- Name & Description -->
        <v-row justify="center" class="px-4">
          <v-text-field
            class="mb-2"
            v-model="measurementName"
            label="Measurement Name"
            variant="outlined"
          />
        </v-row>
        <v-row justify="center" class="px-4">
          <v-textarea
            v-model="measurementDescription"
            label="Description"
            variant="outlined"
            auto-grow
          />
        </v-row>

        <!-- Date & Time -->
        <v-row justify="center">
          <v-time-picker class="text-dark-green" v-model="selectedTime" format="24hr" scrollable />
          <v-date-picker v-model="selectedDate" />
        </v-row>

        <!-- Delta -->
        <v-row justify="center" class="px-4">
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
        <v-row justify="center">
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
        <v-row justify="center" class="my-2">
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
import { mapStores } from 'pinia';
import { useMeasurementStore } from '@/store/MeasurementStore';
import { useModeStore } from '@/store/ModeStore';

export default {
  name: 'NewMeasurementDialog',

  props: {
    type: String,
  },

  data() {
    return {
      dialog: false,
      selectedDate: null,
      selectedTime: null,
      aeDeltaValue: 3,
      aeDeltaUnit: 'Minutes',
      measurementName: '',
      measurementDescription: '',
      showAlert: false,
      errorMessage: 'Invalid measurement setup!',
      rules: {
        required: (value) => !!value || 'Required.',
      },
    };
  },

  computed: {
    ...mapStores(useMeasurementStore),
    ...mapStores(useModeStore),
  },

  methods: {
    scheduleMeasurement() {
      if (this.selectedDate && this.selectedTime) {
        this.dialog = false;
        this.showAlert = false;
        this.selectedDate = null;
        this.selectedTime = null;
      } else {
        this.showAlert = true;
      }
    },

    async startOneTimeMeasurement() {
      if (!this.selectedDate || !this.selectedTime || !this.aeDeltaValue || !this.aeDeltaUnit || !this.measurementName) {
        this.showAlert = true;
        this.errorMessage = 'Please fill in all required fields.';
        return;
      }
    
      const planAt = new Date(this.selectedDate);
      const [hours, minutes] = this.selectedTime.split(':');
      planAt.setHours(parseInt(hours));
      planAt.setMinutes(parseInt(minutes));
      planAt.setSeconds(0);
      planAt.setMilliseconds(0);
    
      const unitMap = {
        Seconds: 1000,
        Minutes: 60000,
        Hours: 3600000,
        Days: 86400000,
      };
    
      const charMap = {
        Seconds: 'S',
        Minutes: 'M',
        Hours: 'H',
        Days: 'D',
      };
    
      const deltaMs = this.aeDeltaValue * unitMap[this.aeDeltaUnit];
      const aeStart = new Date(planAt.getTime() - deltaMs);
      const now = new Date();
    
      if (aeStart < now) {
        this.showAlert = true;
        this.errorMessage = 'AE start time is in the past! Please select a later plan time or smaller delta.';
        return;
      }
    
      const aeDelta = `PT${this.aeDeltaValue}${charMap[this.aeDeltaUnit]}`;
    
      // Custom date string without timezone (in local time)
      const formattedPlanAt = `${planAt.getFullYear()}-${String(planAt.getMonth() + 1).padStart(2, '0')}-${String(planAt.getDate()).padStart(2, '0')}T${String(planAt.getHours()).padStart(2, '0')}:${String(planAt.getMinutes()).padStart(2, '0')}:00`;
    
      const dto = {
        name: this.measurementName,
        description: this.measurementDescription,
        plan_at: formattedPlanAt, // no Z
        ae_delta: aeDelta,
      };
    
      const result = await this.measurementStore.createMeasurement(dto);
    
      if (this.measurementStore.error) {
        this.showAlert = true;
        this.errorMessage = this.measurementStore.error;
      } else {
        this.closeDialog();
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

<style>
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
</style>
