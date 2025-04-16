import { defineStore } from 'pinia';
import axios from 'axios';
import config from '@/config';

export const useMeasurementStore = defineStore('measurement', {
  state: () => ({
    error: null,
    isLoading: false,
    measurements: [],
    measurementDetail: null,
    recordingMode: null,
    status: null,
  }),

  actions: {
    async loadAll() {
      try {
        this.isLoading = true;
        const response = await axios.get(`${config.backendUrl}/measurement`);
        this.measurements = response.data;
        this.error = null;
      } catch (error) {
        this.error = 'Cannot load measurements';
      } finally {
        this.isLoading = false;
      }
    },

    async getMeasurement(id) {
      try {
        this.isLoading = true;
        const response = await axios.get(`${config.backendUrl}/measurement/${id}`);
        this.measurementDetail = response.data;
        this.error = null;
        return response.data;
      } catch (error) {
        this.error = 'Cannot get measurement details';
      } finally {
        this.isLoading = false;
      }
    },

    async createMeasurement(dto) {
      try {
        this.isLoading = true;
        const response = await axios.post(`${config.backendUrl}/measurement`, dto);
        // Pridáme vytvorené meranie do lokálneho zoznamu
        this.measurements.push(response.data);
        this.error = null;
        return response.data;
      } catch (error) {
        this.error = 'Cannot create measurement';
      } finally {
        this.isLoading = false;
      }
    },

    async createPeriodicMeasurement(dto) {
      // TODO: Implement periodic measurement creation logic
    },

    async updateMeasurement(id, dto) {
      try {
        this.isLoading = true;
        const response = await axios.put(`${config.backendUrl}/measurement/${id}`, dto);
        this.error = null;
        // Aktualizujeme meranie v lokálnom zozname
        const index = this.measurements.findIndex((m) => m.id === id);
        if (index !== -1) {
          this.measurements[index] = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = 'Cannot update measurement';
      } finally {
        this.isLoading = false;
      }
    },

    async deleteMeasurement(id) {
      // TODO: Implement measurement deletion logic
    },

    async planMeasurement(id, planAt, aeDelta) {
      // TODO : Implement measurement planning logic
    },

    async unplanMeasurement(id) {
      // TODO : Implement measurement unplanning logic
    },
  },
});
