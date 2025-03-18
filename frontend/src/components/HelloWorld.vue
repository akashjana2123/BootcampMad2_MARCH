<template>
  <div>
    <canvas ref="myChart"></canvas>
  </div>
</template>

<script>
import axios from 'axios';
import  {Chart} from 'chart.js'
import {Chart as ChartJS,Title,Tooltip,Legend,BarElement,BarController,CategoryScale,LinearScale} from 'chart.js';

ChartJS.register(Title,Tooltip,Legend,BarElement,BarController,CategoryScale,LinearScale);

export default{
  data(){
    return{
      chartData:{
        labels:[],
        datasets:[
          {
            label:'number of users',
            backgroundColor: 'blue',
            data:[],
          }
        ]
      },
      chartInstance:null
    }
  },
  mounted(){
    this.fetechUserCounts();
  },
  methods:{
    async fetechUserCounts(){
      try{
        const response = await axios.get('http://127.0.0.1:5000/api/stat')
        const data = response.data;
        this.chartData.labels = Object.keys(data);
        this.chartData.datasets[0].data = Object.values(data)

        this.renderChart();
      } catch(error){
        console.log(error)
      }
    },
    renderChart(){
            if (this.$refs.myChart){
                if (this.chartInstance){
                    this.chartInstance.destroy();
                }
                this.chartInstance = new Chart(this.$refs.myChart.getContext('2d'),{
                    type: 'bar',
                    data:this.chartData,
                    options:{
                        responsive:true,
                        plugins:{
                            legend:{
                                display:true,
                                position:'top',
                            },
                        },
                        scales:{
                            x:{
                                title:{
                                    dispaly:true,
                                    text:'Categories',
                                }
                            }
                        }
                    }
                })
            } else {
                console.error('Chart canvas element not found')
            }
        },
  }
}

</script>