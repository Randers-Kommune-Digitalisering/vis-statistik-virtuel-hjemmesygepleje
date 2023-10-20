<script>
  import { ref, watch } from 'vue';
  import { Chart as ChartJS, ArcElement, BarElement, Tooltip, Legend, CategoryScale, LinearScale } from 'chart.js'
  import { Pie, Bar } from 'vue-chartjs';
  import ChartDataLabels from 'chartjs-plugin-datalabels'

  export default {
    props: {week: String},
    components: { Pie, Bar },
    setup(props) {
      ChartJS.register(ArcElement, BarElement, Tooltip, Legend, CategoryScale, LinearScale, ChartDataLabels)
      const data = ref({})

      updateData(props.week);

      watch(() => props.week, (week) => {
        updateData(week);
      });

      function updateData(week) {
        fetch("/tablets/conversion?week=" + week, { method: "GET" })
        .then(response => response.json())
        .then(res => {
          data.value.nexus_tablets = res.nexus_tablets;
          data.value.citizens = res.citizens;

          let nexus_active = 0;
          res.nexus_tablets.forEach( e => {
            nexus_active += e.available;
          })
          let vitacomm_active = 0;
          res.vitacomm_tablets.forEach( e => {
            vitacomm_active += e.active;
          })
          let citizens_total = 0;
          res.citizens.forEach(e => {
            citizens_total += e.citizens;
          })
          data.value.nexus_units = res.nexus_tablets.map((e) => { return e.unit })
          data.value.nexus_active = nexus_active;
          data.value.vitacomm_active = vitacomm_active;
          data.value.citizens_total = citizens_total;
        });
      };

      return {
        data
      }
    },

    computed: {
      nexusTotalChartData() {
        const with_tablet = this.data.nexus_active;
        const without_tablet = this.data.citizens_total - with_tablet;
        return {
          labels: ['Med skærm', 'Uden skærm'],
          datasets: [
            {
              backgroundColor: ['green', 'red'],
              data: [with_tablet, without_tablet]
            }
          ]
        }
      },
      vitacommTotalChartData() {
        const with_tablet = this.data.vitacomm_active;
        const without_tablet = this.data.citizens_total - with_tablet;
        return {
          labels: ['Med skærm', 'Uden skærm'],
          datasets: [
            {
              backgroundColor: ['green', 'red'],
              data: [with_tablet, without_tablet]
            }
          ]
        }
      },
      nexusUnitChartData() {
        return {
          labels: this.data.nexus_units,
          datasets: [
            {
              label: 'Med skærm',
              backgroundColor: ['green'],
              data: this.data.nexus_tablets.map((e) => { return e['on_loan'] })
            },
            {
              label: 'Uden skærm',
              backgroundColor: ['red'],
              data: this.data.citizens.filter((e) => { if(this.data.nexus_units.includes(e.unit)) return e}).map((e) => {return e.citizens})
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
  <div class="container">
    <div v-if="data.citizens" class="pie-chart-container">
      <h2>Nexus</h2>
      <Pie :data="nexusTotalChartData" :options="pieChartOptions"/>
    </div>
    <div v-if="data.citizens" class="pie-chart-container">
      <h2>Vitacomm</h2>
      <Pie :data="vitacommTotalChartData" :options="pieChartOptions" />
    </div>
    <div v-if="data.citizens" class="bar-chart-container">
      <h2>Nexus</h2>
      <Bar :data="nexusUnitChartData" :options="barChartOptions"/>
    </div>
    <div v-if="data.citizens" class="bar-chart-container">
      <h2>Vitacomm</h2>
      <p>Distrikter i Vitacomm og Nexus passer ikke sammen.</p>
    </div>
  </div>
</template>

<style scoped>
@media (min-width: 1024px) {
  .container {
    display: flex;
    align-items: top;
    flex-direction: row;
  }

  .pie-chart-container {
    max-width: 200px;
    margin-right: 10px;
  }

  .bar-chart-container {
    min-width: 430px;
    height: 400px;
    margin-right: 10px;
  }

  p {
    margin-top: 20px;
  }
}
</style>