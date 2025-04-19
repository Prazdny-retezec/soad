<template>
  <v-dialog max-width="500" v-model="dialog">
    <template v-slot:activator="{ props: activatorProps }">
      <v-icon v-bind="activatorProps" size="20">mdi-eye-outline</v-icon>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card rounded="xl">
        <v-row justify="space-between" class="align-center">
          <v-col class="pr-4" cols="auto">
            <v-card-title class="text-h5">Measurement Information</v-card-title>
          </v-col>
          <v-col class="pr-6" cols="auto">
            <v-icon @click="closeDialog(isActive)" size="30">mdi-close</v-icon>
          </v-col>
        </v-row>

        <!-- DISPLAY MODE -->
        <v-list lines="two" class="ml-2" v-if="detail && !isEditing">
          <v-list-item title="Name" :subtitle="detail.name"></v-list-item>
          <v-list-item title="Description" :subtitle="detail.description"></v-list-item>
          <v-list-item title="Created At" :subtitle="formatDate(detail.created_at)"></v-list-item>
          <v-list-item title="Updated At" :subtitle="formatDate(detail.updated_at)"></v-list-item>
          <v-list-item title="Planned At" :subtitle="formatDate(detail.planned_at)"></v-list-item>
          <v-list-item v-if="detail.started_at" title="Started At" :subtitle="formatDate(detail.started_at)"></v-list-item>
          <v-list-item v-if="detail.ended_at" title="Ended At" :subtitle="formatDate(detail.ended_at)"></v-list-item>
          <v-list-item title="State" :subtitle="detail.state"></v-list-item>
          <v-list-item v-if="detail.result" title="Result" :subtitle="detail.result"></v-list-item>
        </v-list>

        <!-- EDIT MODE -->
        <v-container v-if="detail && isEditing">
          <v-text-field
            v-model="editedName"
            label="Measurement Name"
            variant="outlined"
            class="mb-3"
          />
          <v-textarea
            v-model="editedDescription"
            label="Description"
            variant="outlined"
            auto-grow
          />
        </v-container>

        <!-- ACTION BUTTONS -->
        <v-card-actions v-if="detail">
          <v-spacer></v-spacer>

          <v-btn
            class="mr-2 mb-2"
            variant="tonal"
            color="dark-green"
            v-if="!isEditing"
            :disabled="detail.state === 'PLANNED' || detail.state === 'CANCELLED'"
            @click="handleDownload(detail.id); isActive.value = false"
          >
            Download
          </v-btn>

          <v-btn
            class="mr-2 mb-2"
            variant="outlined"
            color="primary"
            v-if="!isEditing"
            @click="startEditing"
          >
            Edit
          </v-btn>

          <v-btn
            class="mr-2 mb-2"
            variant="tonal"
            color="dark-green"
            v-if="isEditing"
            @click="submitUpdate"
          >
            Save
          </v-btn>

          <v-btn
            class="mr-2 mb-2"
            variant="text"
            color="red"
            v-if="isEditing"
            @click="cancelEditing"
          >
            Cancel
          </v-btn>

          <v-btn
            class="mr-2 mb-2"
            variant="tonal"
            color="secondary"
            v-if="detail.state === 'PLANNED'"
            @click="unplanMeasurement(detail.id)"
          >
            Unplan
          </v-btn>
          <v-btn
            class="mr-2 mb-2"
            variant="tonal"
            color="primary"
            v-if="detail.state === 'NEW'"
            @click="openPlanDialog"
          >
            Plan
          </v-btn>

          <!-- Plan Date Dialog -->
          <v-dialog v-model="planDialog" max-width="500">
            <v-card rounded="xl" class="pa-6">
              <v-card-title class="text-h5">Set Plan Date and Time</v-card-title>
              <v-card-text>
                <!-- Plan From (Date + Time Picker) -->
                <v-card-text class="subtitle text-dark-green font-weight-bold">Plan From</v-card-text>
                <v-row justify="center" class="mb-4">
                  <v-col cols="12">
                    <v-date-picker v-model="selectedDateFrom" class="w-100" />
                  </v-col>
                  <v-col cols="12" class="mt-4">
                    <v-time-picker v-model="selectedTimeFrom" format="24hr" scrollable class="w-100" />
                  </v-col>
                </v-row>

                <!-- AE Delta Section -->
                <v-card-text class="subtitle text-dark-green font-weight-bold">AE Delta</v-card-text>
                <v-row justify="center" class="mb-4">
                  <v-col cols="6">
                    <v-text-field
                      v-model="aeDeltaValue"
                      label="AE Delta Value"
                      type="number"
                      min="1"
                      variant="outlined"
                      class="w-100"
                    />
                  </v-col>
                  <v-col cols="6">
                    <v-select
                      v-model="aeDeltaUnit"
                      label="AE Delta Unit"
                      :items="['Seconds', 'Minutes', 'Hours', 'Days']"
                      variant="outlined"
                      class="w-100"
                    />
                  </v-col>
                </v-row>
              </v-card-text>

              <v-card-actions class="justify-end">
                <v-btn color="primary" variant="tonal" @click="submitPlan" class="mr-2">
                  Save Plan
                </v-btn>
                <v-btn variant="text" @click="planDialog = false">
                  Cancel
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>




        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import Config from '@/config';
import { useMeasurementStore } from '@/store/MeasurementStore';

export default {
  name: 'MeasurementDetail',
  props: {
    measurementId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      detail: null,
      dialog: false,
      isEditing: false,
      editedName: '',
      editedDescription: '',
      planDialog: false,
      selectedDateFrom: null,
      selectedTimeFrom: null,
      aeDeltaValue: 3,
      aeDeltaUnit: 'Days',
  };
  },
  async created() {
    const measurementStore = useMeasurementStore();
    this.detail = await measurementStore.getMeasurement(this.measurementId);
  },
  methods: {
    formatDate(dateString) {
      return dateString ? new Date(dateString).toLocaleString() : 'N/A';
    },
    handleDownload(id) {
      const link = Config.backendUrl + `/measurement/${id}/download`;
      window.open(link);
    },
    closeDialog(isActive) {
      isActive.value = false;
    },
    startEditing() {
      this.editedName = this.detail.name;
      this.editedDescription = this.detail.description;
      this.isEditing = true;
    },
    cancelEditing() {
      this.isEditing = false;
      this.editedName = '';
      this.editedDescription = '';
    },

    // Plan Measurement Method
    openPlanDialog() {
      this.planDialog = true;
    },
    async submitPlan() {
      if (!this.selectedDateFrom || !this.selectedTimeFrom) {
        alert('Please select both date and time.');
        return;
      }

      const planDate = new Date(this.selectedDateFrom);
      const [hours, minutes] = this.selectedTimeFrom.split(':');
      planDate.setHours(parseInt(hours));
      planDate.setMinutes(parseInt(minutes));
      planDate.setSeconds(0);

      let aeDeltaPrefix = 'P';
      const aeDeltaUnitChar = this.aeDeltaUnit.charAt(0);
      if (['H', 'M', 'S'].includes(aeDeltaUnitChar)) aeDeltaPrefix = 'PT';

      const dto = {
        plan_at: planDate.toISOString(),
        ae_delta: `${aeDeltaPrefix}${this.aeDeltaValue}${aeDeltaUnitChar}`,
      };

      console.log('Plánované datum:', dto.plan_at);
      console.log('AE Delta:', dto.ae_delta);

      try {
        const measurementStore = useMeasurementStore();
        await measurementStore.planMeasurement(this.detail.id, dto.plan_at, dto.ae_delta); // opraveno tady!
        this.detail = await measurementStore.getMeasurement(this.detail.id);
        this.planDialog = false;
        alert('Measurement successfully planned.');
      } catch (error) {
        console.error('Error:', error);
        alert('Error planning measurement.');
      }
    },


    async planMeasurement(id, planAt, aeDelta) {
      try {
        this.isLoading = true;
        
        const dto = {
          plan_at: planAt,
          ae_delta: aeDelta,
        };
        
        const response = await axios.post(`${config.backendUrl}/measurement/${id}/plan`, dto);

        const index = this.measurements.findIndex(m => m.id === id);
        if (index !== -1) {
          this.measurements[index] = { ...this.measurements[index], ...response.data };
        }

        this.error = null;
        return response.data;
      } catch (error) {
        this.error = 'Cannot plan measurement';
        console.error('Error planning measurement:', error);
      } finally {
        this.isLoading = false;
      }
    },


    async unplanMeasurement(id) {
      const measurementStore = useMeasurementStore();
      await measurementStore.unplanMeasurement(id);
      this.detail.state = 'NEW';  // Change state to NEW after unplanning
      this.detail.planned_at = null; // Remove planned_at
    },


  },
};
</script>

<style scoped>
.v-text-field,
.v-textarea {
  max-width: 90%;
  margin: 0 auto;
}
</style>
