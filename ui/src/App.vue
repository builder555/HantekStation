<script setup>
import ValueControl from './components/ValueControl.vue';
</script>

<template>
  <header>

  </header>

  <main>
      <ValueControl
        :max="160"
        :coarseStep="1"
        :fineStep="0.05"
        title="voltage"
      />
      <ValueControl
        :max="4.1"
        :coarseStep="0.1"
        :fineStep="0.005"
        title="current"
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
