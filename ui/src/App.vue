<script setup>
import { ref } from 'vue';
import ValueControl from './components/ValueControl.vue';
const voltage = ref(0);
const current = ref(0);
const isOn = ref(false);
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
    <button
      class="onoff"
      :class="isOn ? 'on' : 'off'"
      @click="isOn = !isOn"
    >{{ isOn ? 'on' : 'off' }}</button>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}
.onoff {
  font-size: 3em;
  padding: 0;
  width: 120px;
  height: 120px;
  text-transform: uppercase;
  font-weight: bold;
}
.onoff.on {
  color: #4db1bc;
  text-align: center;
  animation-delay: 0.7s;
  animation: glow 1s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
      text-shadow: 0 0 30px #2d9da9;
    }
    to {
      text-shadow: 0 0 40px #34b3c1, 0 0 20px #4dbbc7;
    }
  }

</style>
<style src="@vueform/slider/themes/default.css"></style>
