<template>
  <v-container fluid>
    <!-- Riadok s filtrami a tlačidlom pre meranie -->
    <v-row class="mb-4" align="center">
      <v-col md="3">
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
        />
      </v-col>
      <v-col md="3">
        <!-- Date order filter (Ascending/Descending) -->
        <v-select
          v-model="selectedTimeFilter"
          :items="dateOrder"
          label="Date"
          item-title="text"
          item-value="value"
          variant="underlined"
          dense
        />
      </v-col>
      <v-col md="6" class="d-flex justify-end">
        <!-- Tlačidlo pre pridanie nového merania -->
        <v-menu open-on-click style="cursor: pointer">
          <template v-slot:activator="{ props }">
            <v-btn color="dark-green" v-bind="props">
              <span class="text-white">Measure</span>
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

    <!-- Table of measurements (full width) -->
    <v-row v-if="filteredMeasurements.length" justify="center">
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
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>
    <!-- Ak nie sú merania -->
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
  name: 'HomeView',
  components: {
    MeasurementDetail,
    NewMeasurementDialog,
  },
  data() {
    return {
      // Filter možností pre stav merania
      stateOptions: [
        { text: 'All', value: 'ALL' },
        { text: 'PLANNED', value: 'PLANNED' },
        { text: 'DONE', value: 'DONE' },
        { text: 'CANCELLED', value: 'CANCELLED' },
      ],
      selectedState: 'ALL',
      // Možnosti zoradenia podľa dátumu
      dateOrder: [
        { text: 'Descending', value: 'DESC' },
        { text: 'Ascending', value: 'ASC' },
      ],
      selectedTimeFilter: 'DESC',
    };
  },
  computed: {
    ...mapState(useMeasurementStore, ['measurements', 'isLoading']),
    filteredMeasurements() {
      let filtered = [...this.measurements];
      // Filter podľa stavu, ak nie je "ALL"
      if (this.selectedState && this.selectedState !== 'ALL') {
        filtered = filtered.filter(
          (measurement) => measurement.state === this.selectedState
        );
      }
      // Zoradenie podľa plánovaného dátumu
      if (this.selectedTimeFilter === 'DESC') {
        filtered.sort((a, b) => new Date(b.planned_at) - new Date(a.planned_at));
      } else if (this.selectedTimeFilter === 'ASC') {
        filtered.sort((a, b) => new Date(a.planned_at) - new Date(b.planned_at));
      }
      return filtered;
    },
  },
  methods: {
    ...mapActions(useMeasurementStore, ['loadAll']),
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
    downloadMeasurement(measurementId) {
      const link = Config.backendUrl + `/measurement/${measurementId}/download`;
      window.open(link);
    },
    refreshTable() {
      this.loadAll();
    },
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
  opacity: 0.5;
  pointer-events: none;
}
</style>
