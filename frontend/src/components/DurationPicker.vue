<template>
  <v-row class="px-4" justify="center">
    <v-col cols="4">
      <v-text-field
          v-model.number="hours"
          label="Hours"
          type="number"
          min="0"
          variant="outlined"
          hide-details
      />
    </v-col>
    <v-col cols="4">
      <v-text-field
          v-model.number="minutes"
          label="Minutes"
          type="number"
          min="0"
          max="59"
          variant="outlined"
          hide-details
      />
    </v-col>
    <v-col cols="4">
      <v-text-field
          v-model.number="seconds"
          label="Seconds"
          type="number"
          min="0"
          max="59"
          variant="outlined"
          hide-details
      />
    </v-col>
  </v-row>
</template>

<script setup>
import {ref, computed, watch, defineProps, defineEmits} from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'PT0S',
  },
})
const emit = defineEmits(['update:modelValue'])

const hours = ref(0)
const minutes = ref(0)
const seconds = ref(0)

watch(
    () => props.modelValue,
    (val) => {
      const match = val?.match(/^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/)
      if (match) {
        hours.value = parseInt(match[1] || 0)
        minutes.value = parseInt(match[2] || 0)
        seconds.value = parseInt(match[3] || 0)
      } else {
        hours.value = 0
        minutes.value = 0
        seconds.value = 0
      }
    },
    {immediate: true}
)

watch([hours, minutes, seconds], () => {
  const h = hours.value || 0
  const m = minutes.value || 0
  const s = seconds.value || 0

  let result = 'PT'
  if (h > 0) result += `${h}H`
  if (m > 0) result += `${m}M`
  if (s > 0) result += `${s}S`
  if (result === 'PT') result += '0S'

  emit('update:modelValue', result)
})
</script>