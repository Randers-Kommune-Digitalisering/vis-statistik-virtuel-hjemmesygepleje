<script>
  import { ref, watch } from 'vue';
  import { Chart as ChartJS, ArcElement, BarElement, Tooltip, Legend, CategoryScale, LinearScale } from 'chart.js'
  import { Pie, Bar } from 'vue-chartjs';
  import ChartDataLabels from 'chartjs-plugin-datalabels'

  export default {
    props: {week: String},
    components: { Pie, Bar},
    setup(props) {
      ChartJS.register(ArcElement, BarElement, Tooltip, Legend, CategoryScale, LinearScale, ChartDataLabels)
      const calls_total = ref({})
      const total_sum_duration = ref(0);
      const total_avg_duration = ref(0);
      const calls_units = ref([])
      const calls_unit_answered = ref([])
      const calls_unit_duration = ref([])

      updateData(props.week);

      watch(() => props.week, (week) => {
        updateData(week);
      });

      function updateData(week) {
        fetch("/calls/citizens?week=" + week, { method: "GET" })
        .then(response => response.json())
        .then(res => {
            console.log(res)
            total_sum_duration.value = res.calls_total[0].sum_duration;
            total_avg_duration.value = res.calls_total[0].avg_duration.split('.')[0];

            calls_total.value = res.calls_total[0];
            calls_units.value = res.calls_unit_answered.map((e) => { return e.unit });
            calls_unit_answered.value = res.calls_unit_answered;
            calls_unit_duration.value = res.calls_unit_duration.map((e) => {e.avg = e.avg.split('.')[0]; return e });
        });
      };

      return {
        calls_total,
        total_sum_duration,
        total_avg_duration,
        calls_units,
        calls_unit_answered,
        calls_unit_duration
      }
    },

    computed: {
      callsTotalChartData() {
        console.log(this.calls_unit_duration)
        let answered = 0;
        let unanswered = 0;
        if(this.calls_total) {
            answered = this.calls_total.answered;
            unanswered = this.calls_total.unanswered;
        }

        return {
          labels: ['Besvaret', 'Ubesvaret'],
          datasets: [
            {
              backgroundColor: ['green', 'red'],
              data: [answered, unanswered]
            }
          ]
        }
      },
      callsAnsweredUnitChartData() {
        return {
          labels: this.calls_units,
          datasets: [
            {
              label: 'Besvaret',
              backgroundColor: ['green'],
              data: this.calls_unit_answered.map((e) => { return e.answered })
            },
            {
              label: 'Ubesvaret',
              backgroundColor: ['red'],
              data: this.calls_unit_answered.map((e) => { return e.unanswered })
            }
          ]
        }
      },
      pieChartOptions() { 
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
                  let percentage = (value*100 / sum).toFixed(0);
                  percentage = percentage > 0 ? percentage+'%' : '';
                  return percentage;
              },
              color: '#fff'
            }
          }
        }
      },
      barChartOptions() { 
        return {
          maintainAspectRatio: false,
          indexAxis: 'y',
          barThickness: 30,
          responsive: true,
          scales: {
            x: {
              stacked: true,
            },
            y: {
              stacked: true
            }
          },
          interaction: {
            mode: 'index'
          },
          plugins: {
            datalabels: {
              formatter: (value, ctx) => {
                const otherDatasetIndex = ctx.datasetIndex === 0 ? 1 : 0;
                const sum =
                  ctx.chart.data.datasets[otherDatasetIndex].data[ctx.dataIndex] + value;
                  let percentage = (value*100 / sum).toFixed(0);
                  percentage = percentage > 0 ? percentage+'%' : '';
                  return percentage
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
  <div v-if="calls_total" class="container">
    <div class="pie-chart-container">
        <Pie :data="callsTotalChartData" :options="pieChartOptions"/>
        <div class="total-duration">
            <span class="bold">Gennemsnit:</span> <span> {{total_avg_duration}}</span><br>
            <span class="bold">Total:</span> <span> {{total_sum_duration}}</span> <br>
            <span class="bold">Planlagt:</span> <span> Distrikter i Vitacomm og Nexus passer ikke sammen.</span>
        </div>
    </div>
    <div class="bar-chart-container">
        <Bar :data="callsAnsweredUnitChartData" :options="barChartOptions"/>
    </div>
    <table>
        <tr>
            <th class="header">Enhed</th>
            <th class="header">Gennemsnit</th>
            <th class="header">Total</th>
            <th class="header">Planlagt</th>
        </tr>
        <tr v-for="item in calls_unit_duration" :key="item">
            <th>{{item.unit}}</th>
            <th>{{item.avg}}</th>
            <th>{{item.sum}}</th>
            <th>Distrikter i Vitacomm og Nexus passer ikke sammen.</th>
        </tr>
    </table>
  </div>
</template>

<style scoped>
@media (min-width: 1024px) {
  .container {
    margin-top: 10px;
    display: flex;
    align-items: top;
    flex-direction: row;
  }

  .pie-chart-container {
    height: 300px;
    max-width: 250px;
    margin-right: 10px;
  }

  .bar-chart-container {
    min-width: 600px;
    height: 320px;
    margin-right: 10px;
    flex-direction: row;
  }

  .total-duration {
    margin-top: 10px;
  }

  .bold {
    font-weight: bold;
    text-decoration: underline;
  }

  p {
    margin-top: 20px;
  }

  table {
    margin-top: 22px;
    height: 320px;
    text-align: left;
  }

  .header {
    text-decoration: underline;
    font-weight: bold;
  }

  th {
    padding-right: 10px;
  }
}
</style>