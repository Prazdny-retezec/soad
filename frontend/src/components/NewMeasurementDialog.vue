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

        <!-- Error Alert (Moved Below Button) -->
        <v-row justify="center" class="my-2 px-4">
          <v-alert
            max-width="100%"
            v-if="showAlert" 
            closable
            :title="errorMessage" 
            type="error"
            variant="tonal"
          ></v-alert>
        </v-row>
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
            max-width="100%"
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
  // Zkontrolujte, zda jsou všechny povinné hodnoty vyplněny
  if (!this.selectedDateFrom || !this.selectedTimeFrom || !this.periodValue || !this.periodUnit || !this.aeDeltaValue || !this.aeDeltaUnit || !this.measurementName) {
    this.showAlert = true;
    this.errorMessage = 'Please fill in all required fields.';
    return;
  }

  // Nastavení data a času pro "plan_from"
  const planFrom = new Date(this.selectedDateFrom);
  const [hoursFrom, minutesFrom] = this.selectedTimeFrom.split(':');
  planFrom.setHours(parseInt(hoursFrom));
  planFrom.setMinutes(parseInt(minutesFrom));
  planFrom.setSeconds(0);
  planFrom.setMilliseconds(0);

  // Kontrola, zda již není naplánováno měření v daném čase
  const conflict = await this.checkForConflictingMeasurements(planFrom);
  if (conflict) {
    this.showAlert = true;
    this.errorMessage = 'A measurement is already scheduled for the selected time.';
    return;
  }

  // Kontrola, zda naplánovaný čas není v minulosti
  const now = new Date();
  if (planFrom <= now) {
    this.showAlert = true;
    this.errorMessage = 'The planned measurement time cannot be in the past.';
    return;
  }

  // Kontrola, zda naplánovaný čas není příliš blízko s ohledem na ae_delta
  const aeDeltaDuration = this.convertToDuration(`PT${this.aeDeltaValue}${this.aeDeltaUnit.charAt(0)}`);
  if (planFrom <= now.getTime() + aeDeltaDuration) {
    this.showAlert = true;
    this.errorMessage = `The planned measurement time is too soon, considering the AE delta of ${this.aeDeltaValue} ${this.aeDeltaUnit}.`;
    return;
  }

  // Nastavení "plan_to" pokud je vyplněno
  const planTo = this.selectedDateTo ? new Date(this.selectedDateTo) : planFrom;
  if (this.selectedDateTo) {
    const [hoursTo, minutesTo] = this.selectedTimeTo.split(':');
    planTo.setHours(parseInt(hoursTo));
    planTo.setMinutes(parseInt(minutesTo));
    planTo.setSeconds(0);
    planTo.setMilliseconds(0);
  }

  // Kontrola, zda "plan_from" je dříve než "plan_to"
  if (planFrom >= planTo) {
    this.showAlert = true;
    this.errorMessage = 'The "From" date and time must be earlier than the "To" date and time.';
    return;
  }

  // **Kontrola počtu opakování**:
  // Vypočteme, jaký je časový rozdíl mezi plan_from a plan_to v milisekundách.
  const timeDiff = planTo - planFrom;

  // Poté spočítáme, kolik opakování se vejde do tohoto časového rámce.
  const periodDuration = this.convertToDuration(`PT${this.periodValue}${this.periodUnit.charAt(0)}`);

  // Vypočteme maximální počet opakování, které se vejdou do časového intervalu
  const maxAllowedPeriods = Math.floor(timeDiff / periodDuration);

  // Pokud je zadaný počet opakování větší než maximální povolený počet, zobrazíme chybu.
  if (this.periodValue > maxAllowedPeriods) {
    this.showAlert = true;
    this.errorMessage = `The number of repetitions exceeds the time frame. You can schedule a maximum of ${maxAllowedPeriods} repetitions.`;
    return;
  }

  // Připravíme hodnoty pro DTO (Data Transfer Object)
  const aeDelta = `PT${this.aeDeltaValue}${this.aeDeltaUnit.charAt(0)}`;
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
    // Odeslání požadavku na backend pro vytvoření měření
    const response = await axios.post(`${Config.backendUrl}/measurement/periodic`, dto);
    console.log('Periodic measurements created successfully:', response.data);

    // Zavřete dialog po úspěšném vytvoření měření
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