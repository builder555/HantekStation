<script setup>
import { ref, computed } from 'vue';
import HalfGauge from './HalfGauge.vue'
import Slider from '@vueform/slider';
const props = defineProps({
  min: {
    type: Number,
    default: 0,
  },
  max: Number,
  coarseStep: Number,
  fineStep: Number,
  title: String,
});
const precision = computed(() => props.fineStep.toString().split('.').slice(-1)[0].length);
const currentValue = ref(props.min);
const minValue = ref(props.min);
const maxValue = ref(props.max);
const mode = ref('coarse');
const step = ref(props.coarseStep);
const fineRange = props.fineStep * 50;
function toggleCorase(newMode) {
  if (newMode === 'coarse') {
    mode.value = 'fine';
    step.value = props.fineStep;
    const campledValue = Math.max(fineRange, Math.min(currentValue.value, props.max - fineRange));
    minValue.value = campledValue - fineRange;
    maxValue.value = campledValue + fineRange;
  } else {
    mode.value = 'coarse';
    step.value = props.coarseStep;
    minValue.value = props.min;
    maxValue.value = props.max;
  }
}
const options = {
  format: {
    to: v => v.toFixed(6),
    from: v => v,
  }
};
</script>
<template>
  <div class="control">
    <HalfGauge
      :title="title"
      :value="currentValue"
      :maxValue="props.max"
      :precision="precision"
    />
    <Slider
      class="slider"
      :tooltips="false"
      :min="minValue"
      :max="maxValue"
      :step="step"
      :lazy="false"
      :options="options"
      v-model="currentValue"
    />
    <button class="coarse-switch" @click="toggleCorase(mode)">{{ mode }}</button>
  </div>
</template>
<style scoped>
.slider {
  --slider-height: 20px; 
  --slider-handle-width: 34px; 
  --slider-handle-height: 34px;
  width: 90%; 
}
.control {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.coarse-switch {
  margin-top: 20px; 
  z-index:1;
  text-transform: uppercase;
}
</style>