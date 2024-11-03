<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import ValueControl from './components/ValueControl.vue';
import { socket } from './websocket';
const realVoltage = ref(0);
const realCurrent = ref(0);
const setVoltage = ref(0);
const setCurrent = ref(0);
const isOn = ref(false);
const maxVoltage = ref(0);
const maxCurrent = ref(0);
const isConnected = ref(false);
const isInitialized = computed(() => 
  maxVoltage.value > 0 && 
  maxCurrent.value > 0 && 
  isConnected.value
);
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
onMounted(() => {
  socket.initSocket();
  socket.on('CONNECTION_STATE', connected => isConnected.value = connected);
  socket.on('POWER', v => isOn.value = v);
  socket.on('VOLTAGE', v => realVoltage.value = v);
  socket.on('CURRENT', v => realCurrent.value = v/1000);
  socket.on('MAX_VOLTAGE', v => maxVoltage.value = v);
  socket.on('MAX_CURRENT', v => maxCurrent.value = v);
  socket.on('VOLTAGE_LIMIT', v => setVoltage.value = v);
  socket.on('CURRENT_LIMIT', v => setCurrent.value = v/1000);
});
watch(setVoltage, throttle(() => {
  socket.send({
    command: 'SET_VOLTAGE',
    payload: setVoltage.value,
  });
}, 200));
watch(setCurrent, throttle(() => {
    socket.send({
      command: 'SET_CURRENT',
      payload: Math.round(setCurrent.value * 1000),
    });
}, 200));  

</script>

<template>
  <div class="status" :class="isConnected ? 'success' : 'error'">{{ isConnected ? 'connected' : 'not connected' }}</div>
  <main v-if="isInitialized">
    <ValueControl
      :max="maxVoltage"
      :coarseStep="1"
      :fineStep="0.05"
      title="voltage"
      :display-value="realVoltage"
      :display-value-if="isOn"
      @start-updating="socket.pauseListener('VOLTAGE_LIMIT')"
      @stop-updating="socket.resumeListener('VOLTAGE_LIMIT')"
      v-model="setVoltage"
    />
    <ValueControl
      :max="maxCurrent"
      :coarseStep="0.1"
      :fineStep="0.005"
      :display-value="realCurrent"
      :display-value-if="isOn"
      title="current"
      @start-updating="socket.pauseListener('CURRENT_LIMIT')"
      @stop-updating="socket.resumeListener('CURRENT_LIMIT')"
      v-model="setCurrent"
    />
  </main>
  <footer>
    <button
      v-if="isConnected"
      class="onoff"
      :class="isOn ? 'on' : 'off'"
      @click="togglePower"
    >{{ isOn ? 'on' : 'off' }}</button>
  </footer>
</template>

<style scoped>
.status {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 99999;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1em;
  height: 30px;
  width: 100%;
  color: white;
}
.status.error {
  background-color: rgba(255, 0, 0, 0.7);
}
.status.success {
  background-color: rgba(0, 255, 0, 0.6);
}

main {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

footer {
  border-top: none;
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
