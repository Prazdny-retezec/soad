<template>
  <v-container fluid v-if="detail != null">
    <!-- Záhlaví -->
    <v-row justify="space-between" class="align-center">
      <v-col cols="auto">
        <h1 class="text-h5">Measurement info - {{ detail.id }}</h1>
      </v-col>
    </v-row>

    <!-- Informace o měření -->
    <v-row>
      <!-- Sloupec 1: Name, Description, State -->
      <v-col cols="12" md="4">
        <v-list lines="two">
          <v-list-item title="Name" :subtitle="detail.name"/>
          <v-list-item title="Description" :subtitle="detail.description"/>
          <v-list-item title="State">
            <state-chip :state="detail.state"/>
          </v-list-item>
        </v-list>
      </v-col>

      <!-- Sloupec 2: Všechny časy -->
      <v-col cols="12" md="4">
        <v-list lines="two">
          <v-list-item title="Created at" :subtitle="formatDate(detail.created_at)"/>
          <v-list-item v-if="detail.updated_at" title="Updated at" :subtitle="formatDate(detail.updated_at)"/>
          <v-list-item v-if="detail.planned_at" title="Planned at" :subtitle="formatDate(detail.planned_at)"/>
          <v-list-item v-if="detail.started_at" title="Started at" :subtitle="formatDate(detail.started_at)"/>
          <v-list-item v-if="detail.ended_at" title="Ended at" :subtitle="formatDate(detail.ended_at)"/>
        </v-list>
      </v-col>

      <!-- Sloupec 3: Výsledek -->
      <v-col cols="12" md="4">
        <v-list lines="two">
          <v-list-item title="Result">
            <file-download-card v-if="detail.result != null"
                                :filename="detail.name + '.zip'"
                                :url="detail.result.cloud_url"/>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>

    <v-divider class="my-6"/>

    <!-- Sensor Settings -->
    <h2 class="text-h5 mb-4">Sensor settings</h2>
    <v-row>
      <!-- RGB Kamera -->
      <v-col cols="12" md="4">
        <h3 class="text-subtitle-1 font-weight-bold mb-2">RGB camera</h3>
        <v-list lines="two" dense>
          <v-list-item title="Quality" :subtitle="detail.sensor_settings.rgb_image_quality  + ' %'"/>
          <v-list-item title="Images count" :subtitle="detail.sensor_settings.rgb_image_count"/>
          <v-list-item title="Width" :subtitle="detail.sensor_settings.rgb_image_width + ' px'"/>
          <v-list-item title="Height" :subtitle="detail.sensor_settings.rgb_image_height + ' px'"/>
          <v-list-item title="Sampling delay" :subtitle="detail.sensor_settings.rgb_sampling_delay + ' s'"/>
        </v-list>
      </v-col>

      <!-- MS Kamera -->
      <v-col cols="12" md="4">
        <h3 class="text-subtitle-1 font-weight-bold mb-2">Multispectral camera</h3>
        <v-list lines="two" dense>
          <v-list-item title="Images count" :subtitle="detail.sensor_settings.ms_image_count"/>
          <v-list-item title="Sampling delay" :subtitle="detail.sensor_settings.ms_sampling_delay + ' s'"/>
        </v-list>
      </v-col>

      <!-- Akustická emise -->
      <v-col cols="12" md="4">
        <h3 class="text-subtitle-1 font-weight-bold mb-2">Acoustic emission</h3>
        <v-list lines="two" dense>
          <v-list-item title="Voltage format" :subtitle="detail.sensor_settings.ae_voltage_format"/>
          <v-list-item title="Voltage dBAE" :subtitle="detail.sensor_settings.ae_voltage_dbae"/>
          <v-list-item title="Counts in log" :subtitle="detail.sensor_settings.ae_counts_log"/>
          <v-list-item title="Counts in lin" :subtitle="detail.sensor_settings.ae_counts_lin"/>
          <v-list-item title="Energy format" :subtitle="detail.sensor_settings.ae_energy_format"/>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import {ref, reactive, onMounted, watch, computed} from 'vue';
import {useMeasurementStore} from '@/store/MeasurementStore';
import Config from '@/config';
import {useRoute} from 'vue-router';
import StateChip from "@/components/StateChip.vue";
import FileDownloadCard from "@/components/FileDownloadCard.vue";
import {de} from "vuetify/locale";

// Refs & state
const route = useRoute()
const measurementId = computed(() => route.params.id);
const detail = ref(null);
const isEditing = ref(false);
const editedName = ref('');
const editedDescription = ref('');
const editedSensorSettings = reactive({});
const planDialog = ref(false);
const selectedDateFrom = ref(null);
const selectedTimeFrom = ref(null);
const aeDeltaValue = ref(3);
const aeDeltaUnit = ref('Days');

// Store
const measurementStore = useMeasurementStore();

// Lifecycle
onMounted(async () => {
  await loadDetail();
});

// Functions
const loadDetail = async () => {
  detail.value = await measurementStore.getMeasurement(measurementId.value);
  if (detail.value?.sensor_settings) {
    Object.assign(editedSensorSettings, detail.value.sensor_settings);
  }
};

const formatDate = (dateString) => {
  return dateString ? new Date(dateString).toLocaleString() : 'N/A';
};

const handleDownload = (id) => {
  const link = `${Config.backendUrl}/measurement/${id}/download`;
  window.open(link);
};

const startEditing = () => {
  editedName.value = detail.value.name;
  editedDescription.value = detail.value.description;
  isEditing.value = true;
  Object.assign(editedSensorSettings, detail.value.sensor_settings);
};

const cancelEditing = () => {
  isEditing.value = false;
  editedName.value = '';
  editedDescription.value = '';
  Object.keys(editedSensorSettings).forEach(key => delete editedSensorSettings[key]);
};

const submitUpdate = async () => {
  const dto = {
    name: editedName.value,
    description: editedDescription.value,
    sensor_settings: {...editedSensorSettings},
  };

  try {
    await measurementStore.updateMeasurement(detail.value.id, dto);
    await loadDetail();
    isEditing.value = false;
    alert('Measurement updated successfully.');
  } catch (error) {
    console.error('Error:', error);
    alert('Error updating measurement.');
  }
};

const openPlanDialog = () => {
  planDialog.value = true;
};

const submitPlan = async () => {
  if (!selectedDateFrom.value || !selectedTimeFrom.value) {
    alert('Please select both date and time.');
    return;
  }

  const planDate = new Date(selectedDateFrom.value);
  const [hours, minutes] = selectedTimeFrom.value.split(':');
  planDate.setHours(parseInt(hours));
  planDate.setMinutes(parseInt(minutes));
  planDate.setSeconds(0);

  let aeDeltaPrefix = 'P';
  const aeDeltaUnitChar = aeDeltaUnit.value.charAt(0);
  if (['H', 'M', 'S'].includes(aeDeltaUnitChar)) aeDeltaPrefix = 'PT';

  const dto = {
    plan_at: planDate.toISOString(),
    ae_delta: `${aeDeltaPrefix}${aeDeltaValue.value}${aeDeltaUnitChar}`,
  };

  try {
    await measurementStore.planMeasurement(detail.value.id, dto.plan_at, dto.ae_delta);
    await loadDetail();
    planDialog.value = false;
    alert('Measurement successfully planned.');
  } catch (error) {
    console.error('Error:', error);
    alert('Error planning measurement.');
  }
};

const unplanMeasurement = async (id) => {
  await measurementStore.unplanMeasurement(id);
  detail.value.state = 'NEW';
  detail.value.planned_at = null;
};
</script>
