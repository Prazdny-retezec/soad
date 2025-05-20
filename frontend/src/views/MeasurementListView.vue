<template>
  <v-container fluid>
    <!-- Row with filters and button for measurement -->
    <v-row class="mb-6 px-4" align="center">
      <v-col cols="12" md="2" class="mb-3 mb-md-0">
        <v-select
            v-model="selectedState"
            :items="stateOptions"
            label="State"
            item-title="text"
            item-value="value"
            variant="underlined"
            hide-details
            dense
            class="w-100"
        />
      </v-col>

      <v-col cols="12" md="10" class="d-flex justify-end">
        <v-menu open-on-click style="cursor: pointer">
          <template #activator="{ props }">
            <v-btn color="dark-green" v-bind="props">
              <span class="text-white">+ Measure</span>
              <v-icon color="white" class="ml-1">mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <new-measurement-dialog type="now"/>
            </v-list-item>
            <v-list-item>
              <new-measurement-dialog type="schedule"/>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>

    <!-- Data table -->
    <v-data-table
        :headers="headers"
        :items="measurements"
        :items-per-page="pagination.itemsPerPage"
        :page="pagination.page"
        :loading="isLoading"
        :server-items-length="totalItems"
        :hover="true"
        @click:row="(_, row) => handleDetailClick(row.item)"
        @update:options="handleOptionsChange">

      <!-- State -->
      <template #item.state="{ item }">
        <state-chip :state="item.state"/>
      </template>

      <!-- Download -->
      <template #item.download="{ item }">
            <span v-if="item.result != null && item.result.cloud_url != null">
              <v-icon
                  @click.stop="handleDownloadRedirect(item)"
                  :class="{ 'disabled-icon': item.state === 'PLANNED' || item.state === 'CANCELLED' }"
                  title='Download'
              >
                mdi-download
              </v-icon>
            </span>
      </template>

      <!-- Delete -->
      <template #item.delete="{ item }">
        <v-icon
            @click.stop="handleDeleteMeasurement(item.id)"
            size="30"
            class="text-red-500"
            :title="'Delete ' + item.name"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>

    <!-- Snackbar -->
    <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        timeout="3000"
        location="bottom left"
    >
      {{ snackbar.text }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import {ref, computed, onMounted, watch} from 'vue';
import {useMeasurementStore} from '@/store/MeasurementStore';
import NewMeasurementDialog from '@/components/NewMeasurementDialog.vue';
import StateChip from "@/components/StateChip.vue";
import router from "@/router";

const stateOptions = [
  {text: 'All', value: 'ALL'},
  {text: 'New', value: 'NEW'},
  {text: 'Planned', value: 'PLANNED'},
  {text: 'Downloading', value: 'DOWNLOADING'},
  {text: 'Zipping', value: 'ZIPPING'},
  {text: 'Uploading', value: 'UPLOADING'},
  {text: 'Error', value: 'ERROR'},
  {text: 'Finished', value: 'FINISHED'},
];

// pagination
const pagination = ref({
  page: 1,
  itemsPerPage: 10,
  sortBy: [],
})
const totalItems = ref(0)
const measurementStore = useMeasurementStore();
const measurements = computed(() => measurementStore.measurements);
const isLoading = computed(() => measurementStore.isLoading);
const selectedState = ref('ALL');

// snackbar state
const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
})

// datatable
const headers = [
  {title: 'Name', key: 'name'},
  {title: 'Created At', key: 'created_at', value: (measurement) => formatDate(measurement.created_at)},
  {title: 'Planned At', key: 'planned_at', value: (measurement) => formatDate(measurement.planned_at)},
  {title: 'State', key: 'state'},
  {title: 'Download', key: 'download', align: 'end', sortable: false},
  {title: 'Delete', key: 'delete', align: 'end', sortable: false}
];

function handleDetailClick(measurement) {
  router.push(`/measurement/${measurement.id}`);
}

function handleDownloadRedirect(measurement) {
  window.open(measurement.result.cloud_url)
}

async function handleDeleteMeasurement(id) {
  try {
    await measurementStore.deleteMeasurement(id);
    refreshTable()

    snackbar.value.text = 'Measurement successfully deleted'
    snackbar.value.color = 'success'
    snackbar.value.show = true
  } catch (error) {
    console.error('Error deleting measurement:', error)
    snackbar.value.text = 'Cannot delete measurement'
    snackbar.value.color = 'error'
    snackbar.value.show = true
  }
}

async function handleOptionsChange(options) {
  pagination.value.page = options.page
  pagination.value.itemsPerPage = options.itemsPerPage

  const sort = options.sortBy?.[0] || {}
  const orderBy = sort.key || null
  const orderDir = sort.order === 'desc' ? 'desc' : 'asc'

  const listingParams = {
    page: options.page,
    pageSize: options.itemsPerPage,
    orderBy,
    orderDir,
  }

  if (selectedState.value !== "ALL") {
    listingParams.state = selectedState.value
  }

  await measurementStore.loadAll(listingParams)
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString();
}

function refreshTable() {
  handleOptionsChange({
    page: pagination.value.page,
    itemsPerPage: pagination.value.itemsPerPage,
    sortBy: pagination.value.sortBy,
  })
}

onMounted(() => {
  measurementStore.loadAll();
});

watch(selectedState, () => {
  refreshTable()
})
</script>

<style scoped>
.filter_wrapper {
  margin-bottom: 16px;
}

.disabled-icon {
  pointer-events: none;
}
</style>
