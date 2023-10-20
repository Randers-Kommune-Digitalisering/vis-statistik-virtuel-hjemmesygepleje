<script setup>
  import { ref } from 'vue';
  import moment from 'moment';
  import conversion from '../components/Conversion.vue'
  import calls from '../components/Calls.vue'

  let lastWeek = new Date();
  lastWeek.setDate(lastWeek.getDate() - 7);
  const yearWeek = ref(lastWeek.getFullYear() + "-W" + (moment(lastWeek).isoWeek()));
</script>

<template>
  <div class="container">
    <input v-model="yearWeek" type="week" class="time-input">
    <h1>Omlægningsgrad</h1>
    <conversion :week="yearWeek" />
    <h1>Opkald</h1>
    <calls :week="yearWeek" />
  </div>
</template>

<style>
  .container {
    display: flex;
    align-items: top;
    flex-direction: column;
  }

  input {
    max-width: 200px;
    padding: 10px;
    border: 1px solid var(--vt-c-grey);
    border-radius: 5px;
    margin-top: 10px;
  }
</style>
