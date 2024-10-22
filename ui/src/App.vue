<script setup>
import HalfGauge from './components/HalfGauge.vue'
</script>

<template>
  <header>

  </header>

  <main>
    <div class="control">
      <HalfGauge 
        title="voltage"
        :value="10" 
        :maxValue="160"
      />
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
