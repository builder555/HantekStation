<script setup>
import { ref } from 'vue';
import ValueControl from './components/ValueControl.vue';
const voltage = ref(0);
const current = ref(0);
</script>

<template>
  <main>
    <ValueControl
      :max="160"
      :coarseStep="1"
      :fineStep="0.05"
      title="voltage"
      v-model="voltage"
    />
    <ValueControl
      :max="4.1"
      :coarseStep="0.1"
      :fineStep="0.005"
      title="current"
      v-model="current"
    />
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: flex-start;
}
</style>
<style src="@vueform/slider/themes/default.css"></style>
