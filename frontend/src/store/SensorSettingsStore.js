import { defineStore } from 'pinia';
import { ref, watch } from 'vue';

export const useSensorSettingsStore = defineStore('sensorSettings', () => {
  const rgbImagesCount = ref(loadNumber('rgbImagesCount', 5));
  const rgbSamplingDelay = ref(loadNumber('rgbSamplingDelay', 1));
  const rgbWidth = ref(loadNumber('rgbWidth', 1920));
  const rgbHeight = ref(loadNumber('rgbHeight', 1080));
  const rgbImageQuality = ref(loadNumber('rgbImageQuality', 75));
  const selectedImageFormat = ref(loadString('selectedImageFormat', 'PNG'));

  const msImagesCount = ref(loadNumber('msImagesCount', 10));
  const msSamplingDelay = ref(loadNumber('msSamplingDelay', 1));

  const selectedVoltageFormat = ref(loadNumber('selectedVoltageFormat', 0));
  const aeCountsLog = ref(loadNumber('aeCountsLog', 1));
  const aeCountsLin = ref(loadNumber('aeCountsLin', 0));
  const aeVoltageDbae = ref(loadBoolean('aeVoltageDbae', false));
  const selectedEnergyFormat = ref(loadNumber('selectedEnergyFormat', 0));
  const aeExportMode = ref(loadString('aeExportMode', 'log'));

  // Watchers pro uložení do localStorage
  watch(rgbImagesCount, val => saveNumber('rgbImagesCount', val));
  watch(rgbSamplingDelay, val => saveNumber('rgbSamplingDelay', val));
  watch(rgbWidth, val => saveNumber('rgbWidth', val));
  watch(rgbHeight, val => saveNumber('rgbHeight', val));
  watch(rgbImageQuality, val => saveNumber('rgbImageQuality', val));
  watch(selectedImageFormat, val => saveString('selectedImageFormat', val));

  watch(msImagesCount, val => saveNumber('msImagesCount', val));
  watch(msSamplingDelay, val => saveNumber('msSamplingDelay', val));

  watch(selectedVoltageFormat, val => saveNumber('selectedVoltageFormat', val));
  watch(aeCountsLog, val => saveNumber('aeCountsLog', val));
  watch(aeCountsLin, val => saveNumber('aeCountsLin', val));
  watch(aeVoltageDbae, val => saveBoolean('aeVoltageDbae', val));
  watch(selectedEnergyFormat, val => saveNumber('selectedEnergyFormat', val));
  watch(aeExportMode, val => saveString('aeExportMode', val));

  // Volitelná metoda
  function setAeExportMode(mode) {
    aeExportMode.value = mode;
  }

  return {
    rgbImagesCount,
    rgbSamplingDelay,
    rgbWidth,
    rgbHeight,
    rgbImageQuality,
    selectedImageFormat,
    msImagesCount,
    msSamplingDelay,
    selectedVoltageFormat,
    aeCountsLog,
    aeCountsLin,
    aeVoltageDbae,
    selectedEnergyFormat,
    aeExportMode,
    setAeExportMode,
  };
});

// ===== Helpers =====

function loadNumber(key, defaultValue) {
  const val = localStorage.getItem(key);
  return val !== null ? Number(val) : defaultValue;
}

function loadString(key, defaultValue) {
  const val = localStorage.getItem(key);
  return val !== null ? val : defaultValue;
}

function loadBoolean(key, defaultValue) {
  const val = localStorage.getItem(key);
  return val !== null ? val === 'true' : defaultValue;
}

function saveNumber(key, val) {
  localStorage.setItem(key, val.toString());
}

function saveString(key, val) {
  localStorage.setItem(key, val);
}

function saveBoolean(key, val) {
  localStorage.setItem(key, val ? 'true' : 'false');
}
