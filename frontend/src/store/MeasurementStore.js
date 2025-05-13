import { defineStore } from 'pinia';
import axios from 'axios';
import config from '@/config';
axios.defaults.baseURL = 'http://localhost:5001'; // or the correct backend URL

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
      try {
        this.isLoading = true;
        
        // Sending a POST request to the backend for creating periodic measurements
        const response = await axios.post(`${config.backendUrl}/measurement/periodic`, dto);
    
        // Assuming the backend will return a list of measurements created
        // We can add them to the local measurements list
        this.measurements.push(...response.data);
        this.error = null;
    
        return response.data;  // Return the created periodic measurements
      } catch (error) {
        this.error = 'Cannot create periodic measurement';
        console.error('Error creating periodic measurement:', error);
      } finally {
        this.isLoading = false;
      }
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
      try {
        this.isLoading = true;
        // Send DELETE request to API for deleting the measurement
        await axios.delete(`${config.backendUrl}/measurement/${id}`);
        
        // Remove the measurement from the local list after successful deletion
        this.measurements = this.measurements.filter((measurement) => measurement.id !== id);
        this.error = null;
      } catch (error) {
        this.error = 'Cannot delete measurement';
        console.error('Error deleting measurement:', error.response || error.message);
      } finally {
        this.isLoading = false;
      }
    },
      

    async planMeasurement(id, planAt, aeDelta) {
      try {
        this.isLoading = true;
        
        const dto = {
          plan_at: planAt,  // datum a čas naplánování
          ae_delta: aeDelta,  // delta pro AE
        };
        
        const response = await axios.post(`${config.backendUrl}/measurement/${id}/plan`, dto);
    
        // Aktualizujeme měření v místním seznamu
        const index = this.measurements.findIndex(m => m.id === id);
        if (index !== -1) {
          this.measurements[index] = { ...this.measurements[index], ...response.data };
        }
    
        this.error = null;
        return response.data;  // nebo "Measurement planned"
      } catch (error) {
        this.error = 'Cannot plan measurement';
        console.error('Error planning measurement:', error);
      } finally {
        this.isLoading = false;
      }
    },
    

    async unplanMeasurement(id) {
      try {
        this.isLoading = true;
        
        const response = await axios.delete(`${config.backendUrl}/measurement/${id}/plan`);
    
        // Aktualizujeme stav měření v místním seznamu
        const index = this.measurements.findIndex(m => m.id === id);
        if (index !== -1) {
          this.measurements[index] = { ...this.measurements[index], ...response.data };
        }
    
        this.error = null;
        return response.data;  // nebo "Measurement unplanned"
      } catch (error) {
        this.error = 'Cannot unplan measurement';
        console.error('Error unplanning measurement:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
  },
});
