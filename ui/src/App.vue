<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import ValueControl from './components/ValueControl.vue';
import { socket } from './websocket';
const isInitialized = computed(() => maxVoltage.value > 0 && maxCurrent.value > 0 && socket.isInitialized);
const voltage = ref(0);
const current = ref(0);
const isOn = ref(false);
const maxVoltage = ref(0);
const maxCurrent = ref(0);
function togglePower() {
  socket.send({
    command: isOn.value ? 'POWER_OFF' : 'POWER_ON',
  });
}
function throttle(fn, wait){
    let throttled = false;
    return function(...args){
        if(!throttled){
          throttled = true;
          setTimeout(()=>{
              fn.apply(this,args);
              throttled = false;
            }, wait);
        }
    }
}
watch(voltage, throttle(() => {
  socket.send({
    command: 'SET_VOLTAGE',
    payload: voltage.value,
  });
}, 200));
watch(current, throttle(() => {
    socket.send({
      command: 'SET_CURRENT',
      payload: Math.round(current.value * 1000),
    });
}, 200));

onMounted(async () => {
  await socket.initSocket();
  socket.on('POWER', v => isOn.value = v);
  // socket.on('VOLTAGE', v => voltage.value = v);
  // socket.on('CURRENT', v => current.value = v);
  socket.on('MAX_VOLTAGE', v => maxVoltage.value = v);
  socket.on('MAX_CURRENT', v => maxCurrent.value = v);
});
</script>

<template>
  <main v-if="isInitialized">
    <ValueControl
      :max="maxVoltage"
      :coarseStep="1"
      :fineStep="0.05"
      title="voltage"
      v-model="voltage"
    />
    <ValueControl
      :max="maxCurrent"
      :coarseStep="0.1"
      :fineStep="0.005"
      title="current"
      v-model="current"
    />
  </main>
  <footer>
    <button
      class="onoff"
      :class="isOn ? 'on' : 'off'"
      @click="togglePower"
    >{{ isOn ? 'on' : 'off' }}</button>
  </footer>
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
  width: 100%;
  height: 100px;
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
