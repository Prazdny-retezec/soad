// src/stores/measurement.ts
import { defineStore } from 'pinia';
import api from '@/services/api.js'
import config from '@/config';


export const useMeasurementStore = defineStore('measurement', {
  state() {
    return {
      error: null,
      isLoading: false,
      status: null,
      recordingMode: null,
      measurements: [],
    };
  },

  actions: {
    async loadAll() {
      this.error = null;
      this.isLoading = true;
      try {
        const { data } = await api.get('/measurement');
        this.measurements = data;
      } catch {
        this.error = 'Cannot load measurements';
      }
    },
    async startAEMeasurement() {
      try {
        this.isLoading = true;
        const response = await axios.post(
          config.backendUrl + '/acoustic/start_rec'
        );
        this.recordingMode = response.data.recording_mode;
        this.status = response.data.status;
        this.error = null;
        this.isLoading = false;
      } catch {
        this.error = 'Cannot start AE measurement';
      }
    },

    async getMeasurement(id) {
      this.error = null;
      this.isLoading = true;
      try {
        const { data } = await api.get(`/measurement/${id}`);
        this.measurementDetail = data;
        return data;
      } catch {
        this.error = 'Cannot get measurement details';
      } finally {
        this.isLoading = false;
      }
    },

    async createMeasurement(dto) {
      this.error = null;
      this.isLoading = true;
      try {
        const { data } = await api.post('/measurement', dto);
        this.measurements.push(data);
        return data;
      } catch {
        this.error = 'Cannot create measurement';
      } finally {
        this.isLoading = false;
      }
    },

    async createPeriodicMeasurement(dto) {
      this.error = null;
      this.isLoading = true;
      try {
        const { data } = await api.post('/measurement/periodic', dto);
        this.measurements.push(...data);
        return data;
      } catch {
        this.error = 'Cannot create periodic measurement';
      } finally {
        this.isLoading = false;
      }
    },

    async updateMeasurement(id, dto) {
      this.error = null;
      this.isLoading = true;
      try {
        const { data } = await api.put(`/measurement/${id}`, dto);
        const idx = this.measurements.findIndex((m) => m.id === id);
        if (idx !== -1) this.measurements[idx] = data;
        return data;
      } catch {
        this.error = 'Cannot update measurement';
      } finally {
        this.isLoading = false;
        this.error = 'Cannot log in, wrong password! Try again.';
      }
    },

    async deleteMeasurement(id) {
      this.error = null;
      this.isLoading = true;
      try {
        await api.delete(`/measurement/${id}`);
        this.measurements = this.measurements.filter((m) => m.id !== id);
      } catch {
        this.error = 'Cannot delete measurement';
      } finally {
        this.isLoading = false;
        this.error = 'Cannot measure RGB photos, check the camera connection.';
      }
    },

    async planMeasurement(id, planAt, aeDelta) {
      this.error = null;
      this.isLoading = true;
      try {
        const dto = { plan_at: planAt, ae_delta: aeDelta };
        const { data } = await api.post(`/measurement/${id}/plan`, dto);
        const idx = this.measurements.findIndex((m) => m.id === id);
        if (idx !== -1) this.measurements[idx] = { ...this.measurements[idx], ...data };
        return data;
      } catch {
        this.error = 'Cannot plan measurement';
      } finally {
        this.isLoading = false;
        this.error = 'Cannot log in, wrong password! Try again.';
      }
    },

    async unplanMeasurement(id) {
      this.error = null;
      this.isLoading = true;
      try {
        const { data } = await api.delete(`/measurement/${id}/plan`);
        const idx = this.measurements.findIndex((m) => m.id === id);
        if (idx !== -1) this.measurements[idx] = { ...this.measurements[idx], ...data };
        return data;
      } catch {
        this.error = 'Cannot unplan measurement';
      } finally {
        this.isLoading = false;
        this.error = 'Cannot log in, wrong password! Try again.';
      }
    },
  },
});
