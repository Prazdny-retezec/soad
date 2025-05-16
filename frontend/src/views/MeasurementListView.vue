<template>
  <v-container fluid>
    <!-- Row with filters and button for measurement -->
    <v-row class="mb-6" align="center px-4" >
      <v-col md="2" class="mb-3 mb-md-0">
        <!-- State filter (All, PLANNED, DONE, CANCELLED) -->
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
      <v-col md="2" class="mb-3 mb-md-0">
        <!-- Date order filter (Ascending/Descending) -->
        <v-select
          v-model="selectedTimeFilter"
          :items="dateOrder"
          label="Date"
          item-title="text"
          item-value="value"
          variant="underlined"
          hide-details
          dense
          class="w-100"
        />
      </v-col>

      <!-- Date Filter with Date Picker -->
      <v-col md="2" class="mb-3 mb-md-0">
        <v-select
          v-model="selectedDateRange"
          :items="[]"
          label="Select Date"
          hint="Click to select a date"
          dense
          hide-details
          class="w-100"
          readonly
          append-outer-icon="mdi-calendar"
          @click="openDatePickerDialog"
        >
          <template v-slot:append>
            <v-icon v-if="selectedDateRange" @click.stop="clearDate">mdi-close-circle</v-icon>
          </template>
        </v-select>
      </v-col>

      <v-col md="6" class="d-flex justify-end">
        <!-- Button for adding new measurement -->
        <v-menu open-on-click style="cursor: pointer">
          <template v-slot:activator="{ props }">
            <v-btn color="dark-green" v-bind="props">
              <span class="text-white">+ Measure</span>
              <v-icon color="white" class="ml-1">mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <new-measurement-dialog type="now" />
            </v-list-item>
            <v-list-item>
              <new-measurement-dialog type="schedule" />
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>

    <!-- Date Picker Dialog -->
    <v-dialog v-model="datePickerDialog" max-width="500" persistent>
      <v-card>
        <v-card-title class="text-h5">Select a Date</v-card-title>
        <v-card-text>
          <v-date-picker v-model="selectedDateRange" @input="confirmDate" />
        </v-card-text>
        <v-card-actions>
          <!-- Cancel Button -->
          <v-btn @click="cancelDateSelection" color="secondary">Cancel</v-btn>
          <!-- Confirm Button -->
          <v-btn @click="confirmDate" color="dark-green">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Table of measurements (full width) -->
    <v-row v-if="filteredMeasurements.length" justify="center" class="px-4">
      <v-col cols="12">
        <v-card elevation="4">
          <v-card-title class="headline d-flex align-center">
            History of measurements
            <v-spacer></v-spacer>
            <!-- Refresh Button on the same row as the title, aligned to the right -->
            <v-btn icon @click="refreshTable" :loading="isLoading" title="Refresh">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-card-title>
          <v-table height="400px" density="comfortable">
            <thead>
              <tr>
                <th>Name</th>
                <th>Planned At</th>
                <th>State</th>
                <th style="text-align: right;">Detail</th>
                <th style="text-align: right;">Download</th>
                <th style="text-align: right;">Delete</th> 
              </tr>
            </thead>
            <tbody>
              <tr v-for="measurement in filteredMeasurements" :key="measurement.id">
                <td class="font-weight-bold">{{ measurement.name }}</td>
                <td>{{ formatDate(measurement.planned_at) }}</td>
                <td>{{ measurement.state }}</td>
                <td align="right">
                  <measurement-detail :measurementId="measurement.id" />
                </td>
                <td align="right">
                  <v-icon
                    :class="{ 'disabled-icon': measurement.state === 'PLANNED' || measurement.state === 'CANCELLED' }"
                    @click="(measurement.state !== 'PLANNED' && measurement.state !== 'CANCELLED') && downloadMeasurement(measurement.id)"
                    :title="measurement.state === 'PLANNED' 
                      ? 'Download disabled for planned measurements' 
                      : measurement.state === 'CANCELLED'
                        ? 'Download disabled for cancelled measurements'
                        : 'Download'"
                  >
                    mdi-download
                  </v-icon>
                </td>
                <!-- DELETE Column with Trash Icon -->
                <td align="right">
                  <v-icon
                    @click="handleDeleteMeasurement(measurement.id)"
                    size="30"
                    class="text-red-500"
                    :title="'Delete ' + measurement.name"
                  >
                    mdi-delete
                  </v-icon>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- If no measurements -->
    <v-row v-else justify="center">
      <v-col cols="12">
        <v-card elevation="4">
          <v-card-title class="headline">
            There are no measurements at this time
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import NewMeasurementDialog from '@/components/NewMeasurementDialog.vue';
import MeasurementDetail from '@/components/MeasurementDetail.vue';
import { mapActions, mapState } from 'pinia';
import { useMeasurementStore } from '@/store/MeasurementStore';
import Config from '@/config';

export default {
  name: 'MeasurementListView',
  components: {
    MeasurementDetail,
    NewMeasurementDialog,
  },
  data() {
    return {
      // Filter options for measurement state
      stateOptions: [
        { text: 'All', value: 'ALL' },
        { text: 'PLANNED', value: 'PLANNED' },
        { text: 'NEW', value: 'NEW' },
        { text: 'DONE', value: 'DONE' },
        { text: 'CANCELLED', value: 'CANCELLED' },
      ],
      selectedState: 'ALL',
      // Date sorting options
      dateOrder: [
        { text: 'Descending', value: 'DESC' },
        { text: 'Ascending', value: 'ASC' },
      ],
      selectedTimeFilter: 'DESC',
      // New date filter
      selectedDateRange: null,
      selectedDateFilter: null,  // Selected date for the date picker
      dateMenu: false, // controls date picker dropdown visibility
      datePickerDialog: false, // controls date picker dialog visibility
    };
  },
  computed: {
    ...mapState(useMeasurementStore, ['measurements', 'isLoading']),
    filteredMeasurements() {
      let filtered = [...this.measurements];

      // Filter by state if not "ALL"
      if (this.selectedState && this.selectedState !== 'ALL') {
        filtered = filtered.filter(
          (measurement) => measurement.state === this.selectedState
        );
      }

      // Filter by selected date range if any
      if (this.selectedDateRange) {
        filtered = filtered.filter(
          (measurement) =>
            new Date(measurement.planned_at).toLocaleDateString() ===
            new Date(this.selectedDateRange).toLocaleDateString()
        );
      }

      // Sort by planned date
      if (this.selectedTimeFilter === 'DESC') {
        filtered.sort((a, b) => new Date(b.planned_at) - new Date(a.planned_at));
      } else if (this.selectedTimeFilter === 'ASC') {
        filtered.sort((a, b) => new Date(a.planned_at) - new Date(b.planned_at));
      }
      return filtered;
    },
  },
  methods: {
    ...mapActions(useMeasurementStore, {
      deleteMeasurement: 'deleteMeasurement',  // Ensure the correct method name here
      loadAll: 'loadAll',
    }),
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
    downloadMeasurement(measurementId) {
      const link = Config.backendUrl + `/measurement/${measurementId}/download`;
      window.open(link);
    },

    async handleDeleteMeasurement(id) {
      try {
        const measurementStore = useMeasurementStore();
        await measurementStore.deleteMeasurement(id);  // Correct method name here
        await measurementStore.loadAll();  // Refresh the list after deletion
        alert('Measurement successfully deleted.');
      } catch (error) {
        console.error('Error deleting measurement:', error);
        alert('Cannot delete measurement');
      }
    },

    refreshTable() {
      this.loadAll();
    },

    // Triggered by dropdown to open the date picker dialog
    openDatePickerDialog() {
      this.dateMenu = false; // Close the menu once date is selected
      this.datePickerDialog = true; // Open the date picker dialog
    },

    // Confirm the date and close the dialog
    confirmDate() {
      this.datePickerDialog = false; // Close the dialog after confirming the date
    },

    // Reset date selection (clear filter)
    cancelDateSelection() {
      this.selectedDateRange = null; // Reset the selected date range
      this.datePickerDialog = false; // Close the dialog without confirming
    },

    // Clear date selection without opening the datepicker again
    clearDate(event) {
      event.stopPropagation(); // Prevent triggering the dropdown again
      this.selectedDateRange = null; // Reset the selected date range
    }
  },
  async mounted() {
    await this.loadAll();
  },
};
</script>

<style scoped>
.filter_wrapper {
  margin-bottom: 16px;
}
.disabled-icon {
  pointer-events: none;
}
</style>
