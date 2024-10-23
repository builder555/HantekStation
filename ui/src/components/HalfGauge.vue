<script setup>
import { computed } from 'vue';
const props = defineProps({
  value: Number,
  maxValue: Number,
  title: String,
  precision: {type: Number, default: 0},
});
const cursorPosition = computed(() => Math.round(props.value / props.maxValue * 9));
const fontSize = computed(() => {
  const numCharacters = `${valueText.value}`.length;
  if (numCharacters > 4) {
    return '1.7em';
  } 
  if (numCharacters > 3) {
    return '2em';
  } 
  return '2.4em';
});
const valueText = computed(() => props.value.toFixed(props.precision));
</script>
<template>
  <div class="gauge-container">
    <div class="gauge">
      <div class="tick-circlebackground"></div>
      <div class="tick-circlegradient"></div>
      <div class="tick-cursor" :style="`--position:${cursorPosition}`"></div>
      <div class="tick-circlegradient-mask"></div>
      <div class="ticks">
        <div style="--tithe-tick-number:1;"></div>
        <div style="--tithe-tick-number:2;"></div>
        <div style="--tithe-tick-number:3;"></div>
        <div style="--tithe-tick-number:4;"></div>
        <div style="--tithe-tick-number:5;"></div>
        <div style="--tithe-tick-number:6;"></div>
        <div style="--tithe-tick-number:7;"></div>
        <div style="--tithe-tick-number:8;"></div>
        <div style="--tithe-tick-number:9;"></div>
        <div style="--tithe-tick-number:10;"></div>
      </div>
      <div class="tick-circle"></div>
      <div class="labels">
        <div class="value-label" :style="{ 'font-size': fontSize }">{{ valueText }}</div>
        <div class="value-title">{{ props.title }}</div>
      </div>
    </div>
  </div>
</template>
<style scoped>
@property --gauge-bg {
  syntax: "<color>";
  inherits: false;
  initial-value: #202b38;
}

.gauge-container {
  margin: 5px;
  text-align: center;
  line-height: 25px;
  font-size: 14px;
  margin-bottom: -50px;
}

.gauge {
  position: relative;
  background: var(--gauge-bg);
  border-radius: 50%;
  min-width: 300px;
  min-height: 300px;
  width:200px;
  height:200px;
  font-size: 34px;
}

.gauge .labels {
  height: 100%;
  color: #ccc;
  font-family: Helvetica, sans-serif;
}

.gauge .labels .value-label {
  position: relative;
  top: 35%;
}

.gauge .labels .value-title {
  position: relative;
  font-size: 1.2em;
  top: 55%;
  text-transform: uppercase;
}

.gauge .tick-cursor {
  position: absolute;
  top: 10%;
  left: 10%;
  width: calc(80%);
  height: calc(80%);
  border-left: 0em solid;
  border-top: 0em solid;
  border-right: 0em solid;
  border-bottom: 0em solid transparent;
  border-radius: 50%;
  background-image: conic-gradient(from clamp(-90deg, calc(-90deg + var(--position)*20deg), 70deg), rgba(250, 0, 250, 0.8) 20deg, transparent 20deg);
}

.gauge .ticks {
  position: absolute;
  width: 100%;
  height: 100%;
}

.gauge .ticks>div {
  transform: rotate(calc(20deg * var(--tithe-tick-number) - 20deg));
  position: relative;
  left: 0%;
  top: 50%;
  width: 100%;
  height: 1%;
  margin-bottom: -1%;
  background: linear-gradient(90deg, rgba(2, 0, 36, 0) 0%, rgba(0, 0, 0, 0) 10%, rgba(0, 0, 0, 1) 10%, rgba(0, 0, 0, 1) 15%, rgba(0, 0, 0, 0) 15%);
}

.gauge .tick-circle {
  --circle-size: 71.2%;
  position: absolute;
  top: 15%;
  left: 14.5%;
  width: var(--circle-size);
  height: var(--circle-size);
  border-left: 0.1em solid #000;
  border-top: 0.1em solid #000;
  border-right: 0.1em solid transparent;
  border-bottom: 0.1em solid transparent;
  border-radius: 50%;
  transform: rotate(44.7deg);
}

.gauge .tick-circlebackground {
  position: absolute;
  top: 0%;
  left: 0%;
  width: 99%;
  height: 99%;
  border: 0em solid;
  border-bottom: 0em solid transparent;
  border-radius: 50%;
  background: var(--gauge-bg);
}

.gauge .tick-circlegradient {
  position: absolute;
  top: 10%;
  left: 10%;
  width: 80%;
  height: 80%;
  border: 0em solid;
  border-bottom: 0em solid transparent;
  border-radius: 50%;
  background-image: conic-gradient(from -90deg, green 0deg, yellow 90deg, red 180deg, transparent 180deg, transparent 360deg);
}

.gauge .tick-circlegradient-mask {
  position: absolute;
  top: 15%;
  left: 15%;
  width: 70%;
  height: 70%;
  border: 0em solid;
  border-bottom: 0em solid transparent;
  border-radius: 50%;
  background: var(--gauge-bg);
}
</style>