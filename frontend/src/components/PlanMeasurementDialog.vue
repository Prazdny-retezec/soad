<template>
  <v-dialog v-model="isOpen" max-width="400">
    <v-card>
      <v-card-title class="ma-2" justify="center">Plan measurement</v-card-title>

      <v-card-text>
        <!-- Date and time -->
        <v-row justify="center">
          <v-col cols="6">
            <v-date-input
                v-model="selectedDate"
                label="Planned at date"
                :prepend-icon="null"
                variant="outlined"
                :hide-actions="true"
                clearable>
            </v-date-input>
          </v-col>
          <v-col cols="6">
            <v-text-field
                v-model="selectedTime"
                label="Planned at time"
                type="time"
                step="60"
                variant="outlined"
                clearable>
            </v-text-field>
          </v-col>
        </v-row>

        <!-- AE delta-->
        <v-row justify="start">
          <v-col cols="12" class="px-4">
            <div class="text-left text-subtitle-1 mb-5">AE delta</div>
            <duration-picker v-model="aeDelta"/>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-spacer/>
        <v-btn color="primary" @click="handleSubmit">Naplánovat</v-btn>
        <v-btn text @click="emit('close')">Zrušit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import {ref, computed} from 'vue';
import DurationPicker from "@/components/DurationPicker.vue";
import { combineDateTime } from '@/util/DatetimeUtil';

const props = defineProps({
  modelValue: Boolean,
});

const emit = defineEmits(['update:modelValue', 'submit', 'close']);

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
});

const selectedDate = ref(null);
const selectedTime = ref(null);
const aeDelta = ref('PT5S');

const handleSubmit = () => {
  if (!selectedDate || !selectedTime) {
    alert('Vyberte datum i čas.');
    return;
  }

  const planAtISO = combineDateTime(selectedDate.value, selectedTime.value)

  emit('submit', {
    plan_at: planAtISO,
    ae_delta: aeDelta.value,
  });

  emit('update:modelValue', false);
};
</script>