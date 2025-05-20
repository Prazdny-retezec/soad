<template>
  <v-container fluid v-if="detail != null">
    <!-- Záhlaví -->
    <v-row justify="space-between" class="align-center">
      <v-col cols="auto">
        <h1 class="text-h5">Measurement info - {{ detail.id }}</h1>
      </v-col>
      <v-col cols="auto">
        <v-btn v-if="detail.state === 'NEW'" color="primary" @click="openPlanDialog">
          Plan
        </v-btn>
        <v-btn v-if="detail.state === 'PLANNED'" color="warning" @click="unplanMeasurement(detail.id)">
          Unplan
        </v-btn>
        <v-btn v-if="!isEditing" color="grey-darken-1" class="ms-3" @click="startEditing">
          Edit
        </v-btn>
        <template v-if="isEditing">
          <v-btn color="success" @click="submitUpdate" class="ms-3 me-3">Save</v-btn>
          <v-btn color="error" @click="cancelEditing">Cancel</v-btn>
        </template>
      </v-col>
    </v-row>

    <!-- Informace o měření -->
    <v-row>
      <!-- Sloupec 1: Name, Description, State -->
      <v-col cols="12" md="4">
        <v-list lines="two">
          <v-list-item title="Name">
            <template #subtitle>
              <div v-if="!isEditing">{{ detail.name }}</div>
              <v-text-field v-else v-model="editedName" dense hide-details/>
            </template>
          </v-list-item>
          <v-list-item title="Description">
            <template #subtitle>
              <div v-if="!isEditing">{{ detail.description }}</div>
              <v-textarea v-else v-model="editedDescription" rows="2" dense hide-details/>
            </template>
          </v-list-item>
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

  <plan-measurement-dialog
      v-model="planDialog"
      @submit="handlePlanSubmit"
      @close="planDialog = false"
  />
</template>

<script setup>
import {ref, reactive, onMounted, watch, computed} from 'vue';
import {useMeasurementStore} from '@/store/MeasurementStore';
import Config from '@/config';
import {useRoute} from 'vue-router';
import StateChip from "@/components/StateChip.vue";
import FileDownloadCard from "@/components/FileDownloadCard.vue";
import PlanMeasurementDialog from '@/components/PlanMeasurementDialog.vue';

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
  try {
    const data = await measurementStore.getMeasurement(measurementId.value);
    if (!data) {
      alert('Not found');
      return;
    }
    detail.value = data;
    if (data.sensor_settings) {
      Object.assign(editedSensorSettings, data.sensor_settings);
    }
  } catch (error) {
    console.error('Chyba při načítání detailu:', error);
  }
};

const formatDate = (dateString) => {
  return dateString ? new Date(dateString).toLocaleString() : 'N/A';
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
    description: editedDescription.value
  };

  try {
    await measurementStore.updateMeasurement(detail.value.id, dto);
    await loadDetail();
    isEditing.value = false;
  } catch (error) {
    console.error('Error:', error);
  }
};

const openPlanDialog = () => {
  planDialog.value = true;
};

const handlePlanSubmit = async ({plan_at, ae_delta}) => {
  try {
    await measurementStore.planMeasurement(detail.value.id, plan_at, ae_delta);
    await loadDetail();
  } catch (error) {
    console.error('Chyba při plánování:', error);
  }
};

const unplanMeasurement = async (id) => {
  await measurementStore.unplanMeasurement(id);
  detail.value.state = 'NEW';
  detail.value.planned_at = null;
};
</script>
