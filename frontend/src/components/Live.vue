<script>
  import { ref, watch } from 'vue';
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
  import { Pie } from 'vue-chartjs';
  import ChartDataLabels from 'chartjs-plugin-datalabels'

  export default {
    components: { Pie },
    setup() {
      ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels)
      const live_data = ref({knox_active: 0, knox_total: 0, vitacomm_active: 0, vitacomm_total: 0})

      fetch("/tablets/active", { method: "GET" })
      .then(response => response.json())
      .then(data => {
        live_data.value = data.active_now[0];
      });

      return {
        live_data
      }
    },

    computed: {
      knoxChartData() {
        const active = this.live_data.knox_active;
        const inactive = this.live_data.knox_total - active;
        return {
          labels: ['Aktive', 'Inaktive'],
          datasets: [
            {
              backgroundColor: ['green', 'red'],
              data: [active, inactive]
            }
          ]
        }
      },
      vitacommChartData() {
        const active = this.live_data.vitacomm_active;
        const inactive = this.live_data.vitacomm_total - active;
        return {
          labels: ['Aktive', 'Inaktive'],
          datasets: [
            {
              backgroundColor: ['green', 'red'],
              data: [active, inactive]
            }
          ]
        }
      },
      ChartOptions() { 
        return {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            datalabels: {
              formatter: (value, dnct1) => {
                  let sum = 0;
                  let dataArr = dnct1.chart.data.datasets[0].data;
                  dataArr.map(data => {
                      sum += data;
                  });
                  let percentage = (value*100 / sum).toFixed(2)+'%';
                  return [value, percentage];
              },
              color: '#fff'
            }
          }
        }
      }
    }
  }
</script>

<template>
  <div class="live">
    <div class="chart-container">
      <h2>Samsung skærme: {{live_data.knox_total}}</h2>
      <Pie :data="knoxChartData" :options="ChartOptions"/>
      <p>*Skærm er regnet aktiv hvis den er set tændt inden for de sidste 7 dage.</p>
    </div>
    <div class="chart-container">
      <h2>Vitacomm skærme: {{live_data.vitacomm_total}}</h2>
      <Pie :data="vitacommChartData" :options="ChartOptions" />
      <p>*Skærm er regnet aktiv hvis der har været et besvaret opkald inden for de sidste 7 dage.</p>
    </div>
  </div>
</template>

<style scoped>
@media (min-width: 512px) {
  .live {
    display: flex;
    align-items: top;
    flex-direction: row;
  }

  .chart-container {
    max-width: 200px;
    margin-right: 200px;
  }

  p {
    margin-top: 20px;
  }
}
</style>
