<template>
  <v-container fluid>
    <h2 class="text-h4 ma-4 mb-10 text-center">Default sensor settings</h2>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <div class="tabs">
          <div :class="{ active: activeTab === 'rgbCamera' }" @click="activeTab = 'rgbCamera'">RGB Camera</div>
          <div :class="{ active: activeTab === 'multispectralCamera' }" @click="activeTab = 'multispectralCamera'">
            Multispectral Camera
          </div>
          <div :class="{ active: activeTab === 'acousticEmission' }" @click="activeTab = 'acousticEmission'">Acoustic
            Emission
          </div>
        </div>
        <v-card>
          <div class="tab-content">
            <div v-if="activeTab === 'rgbCamera'">
              <v-card-title class="headline">Measurement Configuration - RGB Camera</v-card-title>
              <v-table density="compact" colspan="2">
                <tbody>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">Number of RGB images</div>
                    <v-row align="center">
                      <v-col cols="12">
                        <v-slider v-model="rgbImagesCount" append-icon="mdi-image"
                                  thumb-color=#82C325 show-ticks="always" step="5"
                                  tick-size="3" thumb-label></v-slider>
                      </v-col>
                    </v-row>
                  </td>
                </tr>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">Sampling delay</div>
                    <v-row align="center">
                      <v-col cols="12">
                        <v-text-field class="my-2" label="Set delay between captures (s)" v-model="rgbSamplingDelay"
                                      :rules="[rules.numberFormat]"></v-text-field>
                      </v-col>
                    </v-row>
                  </td>
                </tr>
                <tr class="align-center">
                  <td class="align-center" colspan="1">
                    <div class="text-subtitle-1">Image width</div>
                    <v-row align="center">
                      <v-col cols="12">
                        <v-text-field class="my-2" label="Set image width (px)" v-model="rgbWidth"
                                      :rules="[rules.numberFormat]"></v-text-field>
                      </v-col>
                    </v-row>
                  </td>
                  <td class="align-center" colspan="1">
                    <div>
                      <div class="text-subtitle-1">Image height</div>
                      <v-row align="center">
                        <v-col cols="12">
                          <v-text-field class="my-2" label="Set image height (px)" v-model="rgbHeight"
                                        :rules="[rules.numberFormat]"></v-text-field>
                        </v-col>
                      </v-row>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">Image quality</div>
                    <v-row align="center">
                      <v-col cols="12">
                        <v-slider v-model="rgbImageQuality"
                                  thumb-color=#82C325 show-ticks="always" step="5"
                                  tick-size="3" thumb-label></v-slider>
                      </v-col>
                    </v-row>
                  </td>
                </tr>
                <tr>
                  <td class="align-center" colspan="2">
                    <v-row align="center">
                      <v-col cols="12">
                        <v-select
                            v-model="selectedImageFormat"
                            :items="imageFormats"
                            label="Image format"
                            item-title="text"
                            item-value="value"
                            variant="underlined"
                            hide-details
                            dense
                            class="w-100 pa-2"
                        />
                      </v-col>
                    </v-row>
                  </td>
                </tr>
                </tbody>
              </v-table>
            </div>
            <div v-if="activeTab === 'multispectralCamera'">
              <v-card-title class="headline">Measurement Configuration - Multispectral Camera</v-card-title>
              <v-table density="compact" colspan="2">
                <tbody>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">Number of MS images</div>
                    <v-row align="center">
                      <v-col cols="12">
                        <v-slider v-model="msImagesCount" append-icon="mdi-image"
                                  thumb-color=#82C325 show-ticks="always" step="1"
                                  tick-size="3" max="20" thumb-label></v-slider>
                      </v-col>
                    </v-row>
                  </td>
                </tr>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">Sampling delay</div>
                    <v-row align="center">
                      <v-col cols="12">
                        <v-text-field class="my-2" label="Set delay between captures (s)" v-model="msSamplingDelay"
                                      :rules="[rules.numberFormat]"></v-text-field>
                      </v-col>
                    </v-row>
                  </td>
                </tr>
                </tbody>
              </v-table>
            </div>
            <div v-if="activeTab === 'acousticEmission'">
              <v-card-title class="headline">Measurement Configuration - Acoustic Emission</v-card-title>
              <v-table density="compact" colspan="2">
                <tbody>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">Voltage format</div>
                    <v-row align="center">
                      <v-col cols="12">
                        <v-select
                            v-model="selectedVoltageFormat"
                            :items="voltageFormats"
                            item-title="text"
                            item-value="value"
                            variant="underlined"
                            hide-details
                            dense
                            class="w-100 pa-2"/>
                      </v-col>
                    </v-row>
                  </td>
                </tr>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">AE export mode</div>
                    <v-radio-group v-model="aeExportMode">
                      <v-radio label="Logarithmic" value="log"/>
                      <v-radio label="Linear" value="lin"/>
                    </v-radio-group>
                  </td>
                </tr>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">dBAE</div>
                    <v-checkbox
                        v-model="aeVoltageDbae"
                        label="Export AE voltage in dBAE"
                    />
                  </td>
                </tr>
                <tr>
                  <td class="align-center" colspan="2">
                    <div class="text-subtitle-1">Energy format</div>
                    <v-row align="center">
                      <v-col cols="5">
                        <v-select
                            v-model="selectedEnergyFormat"
                            :items="energyFormats"
                            item-title="text"
                            item-value="value"
                            variant="underlined"
                            hide-details
                            dense
                            class="w-100 pa-2"/>
                      </v-col>
                    </v-row>
                  </td>
                </tr>
                </tbody>
              </v-table>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "SensorSettingsView",
  data() {
    return {
      activeTab: 'rgbCamera',
      rgbImagesCount: 10,
      rgbSamplingDelay: 30,
      rgbWidth: 1920,
      rgbHeight: 1080,
      rgbImageQuality: 90,
      imageFormats: [
        {text: 'TIFF', value: 'TIFF'},
        {text: 'PNG', value: 'PNG'},
        {text: 'RAW', value: 'RAW'},
      ],
      selectedImageFormat: {text: 'PNG', value: 'PNG'},
      msImagesCount: 2,
      msSamplingDelay: 30,
      voltageFormats: [
        {text: 'not exported', value: 0},
        {text: 'nano Volts', value: 1},
        {text: 'micro Volts (integer)', value: 2},
        {text: 'micro Volts (float)', value: 3},
        {text: 'milli Volts', value: 4},
        {text: 'Volts', value: 5},
      ],
      selectedVoltageFormat: {text: 'Volts', value: 5},
      aeCountsLog: 1,
      aeCountsLin: 0,
      aeExportMode: 'log',
      aeVoltageDbae: false,
      energyFormats: [
        {text: 'V^2/Hz', value: 0},
        {text: 'uV^2/Hz', value: 1},
      ],
      selectedEnergyFormat: {text: 'uV^2/Hz', value: 1},
      formValid: true,
      rules: {
        required: value => !!value || 'Required.',
        numberFormat: value => /^\d+(\.\d+)?$/.test(value) || 'Invalid number format'
      },
    }
  },
  watch: {
    aeExportMode(newVal) {
      if (newVal === 'log') {
        this.ae_counts_log = 1
        this.ae_counts_lin = 0
      } else {
        this.ae_counts_log = 0
        this.ae_counts_lin = 1
      }
    }
  }
}
</script>

<style>
.tabs {
  display: flex;
}

.tabs div {
  padding: 10px;
  cursor: pointer;
  border: 0.5px solid rgba(204, 204, 204, 0.44);
  border-bottom: none;
  border-radius: 5px;
  margin-right: 2mm;
  background-color: #f2f2f2;
  transition: box-shadow 0.3s, opacity 0.3s, background-color 0.3s, height 0.3s;
}

.tabs div.active {
  font-weight: bold;
  border-radius: 5px 5px 0 0;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  opacity: 1;
}

.text-subtitle-1 {
  margin-top: 10px;
}
</style>
