<script setup>
import { ref } from 'vue';
import HalfGauge from './components/HalfGauge.vue'
import Slider from '@vueform/slider';
const voltage = ref(0);
const maxVoltage = 160;
</script>

<template>
  <header>

  </header>

  <main>
    <div class="control">
      <HalfGauge 
        title="voltage"
        :value="voltage" 
        :maxValue="maxVoltage"
      />
      <Slider v-model="voltage" :min="0" :max="maxVoltage" :lazy="false"/>
    </div>
    <div class="control">
      <HalfGauge 
        title="current"
        :value="1.55" 
        :maxValue="4.1"
      />
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}
</style>
<style src="@vueform/slider/themes/default.css"></style>