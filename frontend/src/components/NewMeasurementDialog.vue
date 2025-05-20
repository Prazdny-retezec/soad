<template>
  <v-dialog max-width="700" v-model="dialog">
    <template v-slot:activator="{ props: activatorProps }">
      <div v-bind="activatorProps">
        <span v-if="type === 'schedule'">Periodic schedule</span>
        <span v-else>One-time measurement</span>
      </div>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card :title="props.type === 'schedule' ? 'Create periodic schedule' : 'Create one-time measurement'"
              rounded="xl" class="text-center">
        <!-- Name -->
        <v-row justify="center" class="mb-0 px-4">
          <v-text-field v-model="name" label="Name" variant="outlined" class="w-100"/>
        </v-row>

        <!-- Description -->
        <v-row justify="center" class="px-4">
          <v-textarea v-model="description" label="Description" variant="outlined" auto-grow class="w-100"/>
        </v-row>

        <!-- Duration-->
        <v-row justify="start">
          <v-col cols="12">
            <h3 class="text-left mb-5">Duration</h3>
            <duration-picker v-model="duration"/>
          </v-col>
        </v-row>

        <!-- Planning checkbox -->
        <template v-if="props.type !== 'schedule'">
          <v-row justify="start" class="mb-2 px-4">
            <v-checkbox
                v-model="planningEnabled"
                label="Plan this measurement"
                color="dark-green"
                hide-details
            ></v-checkbox>
          </v-row>
        </template>

        <!-- Conditional Planning fields -->
        <template v-if="(props.type === 'schedule') || planningEnabled">
          <template v-if="props.type === 'schedule'">
            <!-- Periodic planning inputs -->
            <h3 class="text-left mb-5">Plan from</h3>
            <v-row justify="center">
              <v-col cols="6">
                <v-date-input
                    v-model="selectedDateFrom"
                    label="Plan from (date)"
                    :prepend-icon="null"
                    variant="outlined"
                    :hide-actions="true"
                    clearable>
                </v-date-input>
              </v-col>
              <v-col cols="6">
                <v-text-field
                    v-model="selectedTimeFrom"
                    label="Plan from (time)"
                    type="time"
                    step="60"
                    variant="outlined"
                    clearable>
                </v-text-field>
              </v-col>
            </v-row>

            <h3 class="text-left mb-5">Plan to</h3>
            <v-row justify="center">
              <v-col cols="6">
                <v-date-input
                    v-model="selectedDateTo"
                    label="Plan to (date)"
                    :prepend-icon="null"
                    variant="outlined"
                    :hide-actions="true"
                    clearable>
                </v-date-input>
              </v-col>
              <v-col cols="6">
                <v-text-field
                    v-model="selectedTimeTo"
                    label="Plan to (time)"
                    type="time"
                    step="60"
                    variant="outlined"
                    clearable>
                </v-text-field>
              </v-col>
            </v-row>

            <v-row justify="start">
              <v-col cols="12" class="px-4">
                <h3 class="text-left mb-5">Period</h3>
                <duration-picker v-model="period"/>
              </v-col>
            </v-row>
          </template>
          <template v-else>
            <h3 class="text-left mb-5">Plan at</h3>
            <v-row justify="center">
              <v-col cols="6">
                <v-date-input
                    v-model="selectedDate"
                    label="Plan at (date)"
                    :prepend-icon="null"
                    variant="outlined"
                    :hide-actions="true"
                    clearable>
                </v-date-input>
              </v-col>
              <v-col cols="6">
                <v-text-field
                    v-model="selectedTime"
                    label="Plan at (time)"
                    type="time"
                    step="60"
                    variant="outlined"
                    clearable>
                </v-text-field>
              </v-col>
            </v-row>
          </template>

          <!-- AE delta (common for both modes) -->
          <v-row justify="start">
            <v-col cols="12" class="px-4">
              <h3 class="text-left mb-5">AE delta</h3>
              <duration-picker v-model="aeDelta"/>
            </v-col>
          </v-row>
        </template>

        <!-- SensorsSettings checkbox -->
        <v-row justify="start" class="mb-2 px-4">
          <v-checkbox
              v-model="useDefaultSensorSettings"
              label="Use default sensor settings"
              color="dark-green"
              hide-details
          ></v-checkbox>
        </v-row>

        <!-- Conditional SensorSettings fields -->
        <template v-if="!useDefaultSensorSettings">
          <!-- RGB Camera Section -->
          <section class="settings-section">
            <h3>RGB Camera</h3>
            <v-text-field v-model.number="sensorSettings.rgb_image_quality" label="RGB Image Quality" type="number" min="1" max="100"/>
            <v-text-field v-model.number="sensorSettings.rgb_image_count" label="RGB Image Count" type="number" min="1"/>
            <v-text-field v-model.number="sensorSettings.rgb_image_width" label="RGB Image Width" type="number" min="1"/>
            <v-text-field v-model.number="sensorSettings.rgb_image_height" label="RGB Image Height" type="number" min="1"/>
            <v-text-field v-model.number="sensorSettings.rgb_sampling_delay" label="RGB Sampling Delay (sec)" type="number" min="0"/>
          </section>

          <!-- Multispectral Camera Section -->
          <section class="settings-section">
            <h3>Multispectral Camera</h3>
            <v-text-field v-model.number="sensorSettings.ms_image_count" label="MS Image Count" type="number" min="1"/>
            <v-text-field v-model.number="sensorSettings.ms_sampling_delay" label="MS Sampling Delay (sec)" type="number" min="0"/>
          </section>

          <!-- Acoustic Emission Section -->
          <section class="settings-section">
            <h3>Acoustic Emission</h3>
            <v-text-field v-model.number="sensorSettings.ae_voltage_format" label="AE Voltage Format" type="number"/>
            <v-text-field v-model.number="sensorSettings.ae_voltage_dbae" label="AE Voltage DBAE" type="number"/>
            <v-text-field v-model.number="sensorSettings.ae_counts_log" label="AE Counts Log" type="number"/>
            <v-text-field v-model.number="sensorSettings.ae_counts_lin" label="AE Counts Lin" type="number"/>
            <v-text-field v-model.number="sensorSettings.ae_energy_format" label="AE Energy Format" type="number"/>
          </section>
        </template>

        <!-- Start Button -->
        <v-row justify="center" class="mb-4 px-4">
          <v-btn color="dark-green" rounded="xl" class="my-4" @click="createMeasurement">
            Add measurement
          </v-btn>
        </v-row>

        <!-- Error Alert -->
        <v-row justify="center" class="my-2 px-4">
          <v-alert max-width="100%" v-if="showAlert" closable :title="errorMessage" type="error" variant="tonal"/>
        </v-row>
      </v-card>
    </template>
  </v-dialog>

</template>

<script setup>
import {ref, reactive, onMounted, watch} from 'vue';
import DurationPicker from '@/components/DurationPicker.vue';
import {useMeasurementStore} from '@/store/MeasurementStore';
import {useSensorSettingsStore} from "@/store/SensorSettingsStore";
import {combineDateTime} from '@/util/DatetimeUtil';

// Props
const props = defineProps({
  type: String,
});

// emit
const emit = defineEmits(['submitted'])

// Store
const measurementStore = useMeasurementStore();
const sensorSettingsStore = useSensorSettingsStore()

const dialog = ref(false);

// Stav formuláře
const name = ref('');
const description = ref('');
const planningEnabled = ref(false);
const useDefaultSensorSettings = ref(true);

const duration = ref('PT1M');
const aeDelta = ref('PT5S');
const period = ref('PT1H')

const selectedDateFrom = ref(null);
const selectedTimeFrom = ref(null);
const selectedDateTo = ref(null);
const selectedTimeTo = ref(null);

const selectedDate = ref(null);
const selectedTime = ref(null);

const showAlert = ref(false);
const errorMessage = ref('');
const isLoading = ref(false);

// Sensor settings
const sensorSettings = reactive({
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
});

function closeDialog() {
  dialog.value = false;
  resetForm();
}

function resetForm() {
  name.value = '';
  description.value = '';
  planningEnabled.value = false;
  useDefaultSensorSettings.value = true;
  duration.value = 'PT1M';
  aeDelta.value = 'PT5S';
  selectedDateFrom.value = null;
  selectedTimeFrom.value = null;
  selectedDateTo.value = null;
  selectedTimeTo.value = null;
  selectedDate.value = null;
  selectedTime.value = null;
  showAlert.value = false;
  errorMessage.value = '';
  isLoading.value = false;
}

function loadSensorDefaultsFromStore() {
  Object.assign(sensorSettings, {
    rgb_image_quality: sensorSettingsStore.rgbImageQuality,
    rgb_image_count: sensorSettingsStore.rgbImagesCount,
    rgb_image_width: sensorSettingsStore.rgbWidth,
    rgb_image_height: sensorSettingsStore.rgbHeight,
    rgb_sampling_delay: sensorSettingsStore.rgbSamplingDelay,
    ms_image_count: sensorSettingsStore.msImagesCount,
    ms_sampling_delay: sensorSettingsStore.msSamplingDelay,
    ae_voltage_format: sensorSettingsStore.selectedVoltageFormat,
    ae_voltage_dbae: sensorSettingsStore.aeVoltageDbae ? 1 : 0,
    ae_counts_log: sensorSettingsStore.aeCountsLog,
    ae_counts_lin: sensorSettingsStore.aeCountsLin,
    ae_energy_format: sensorSettingsStore.selectedEnergyFormat,
  });
}

async function createMeasurement() {
  showAlert.value = false;
  errorMessage.value = '';

  if (!name.value) {
    showAlert.value = true;
    errorMessage.value = 'Name is required';
    return;
  }

  const common = {
    name: name.value,
    description: description.value,
    duration: duration.value,
    ae_delta: aeDelta.value,
    sensor_settings: sensorSettings
  };

  let dto;

  try {
    if (props.type === 'schedule') {
      const planFrom = combineDateTime(selectedDateFrom.value, selectedTimeFrom.value);
      const planTo = combineDateTime(selectedDateTo.value, selectedTimeTo.value);

      if (!planFrom || !planTo || !period.value) {
        showAlert.value = true;
        errorMessage.value = 'Plan from, to, and period must be specified';
        return;
      }

      dto = {
        ...common,
        plan_from: planFrom,
        plan_to: planTo,
        period: period.value
      };

      await measurementStore.createPeriodicMeasurement(dto);
    } else {
      // One-time
      const planAt = planningEnabled.value
          ? combineDateTime(selectedDate.value, selectedTime.value)
          : null;

      dto = {
        ...common,
        plan_at: planAt
      };

      await measurementStore.createMeasurement(dto);
    }

    emit('submitted');
    closeDialog();
  } catch {
    showAlert.value = true;
    errorMessage.value = measurementStore.error || 'Unknown error';
  }
}

// lifecycle
watch(useDefaultSensorSettings, (newValue) => {
  if (newValue) {
    loadSensorDefaultsFromStore();
  }
});

onMounted(() => {
  if (useDefaultSensorSettings.value) {
    loadSensorDefaultsFromStore();
  }
});

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