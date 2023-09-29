<template>
    <div class = "maintext">
        <el-tabs class="demo-tabs" @tab-click="handleClick" tabPosition="top" v-model="activeTab">
            <el-tab-pane label="流水分析" name="first">
            <div class="chart">
                <div ref="chartContainer" style="width: 600px; height: 550px;"></div>
                <div ref="chartContainer2" style="width: 600px; height: 500px;"></div>
            </div>

            <el-divider><el-icon><star-filled /></el-icon></el-divider>

            <el-alert title="以下是本月已有流水数据" type="success" close-text="Delete"/>
            <TableOne/>
            </el-tab-pane>
            <el-tab-pane label="场内车辆" name="second">
            
            </el-tab-pane>
            <el-tab-pane label="停车记录" name="third">
            

            </el-tab-pane>
        </el-tabs>
    </div>
</template>
  
<script>
import { ref, onMounted} from 'vue';
import * as echarts from 'echarts/core';
import {
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components';
import { BarChart, LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import TableOne from '../subcomponents/TableOne.vue'


export default {
    methods: {
        handleClick(tab, event) {
        console.log(tab, event);
        },
    },
    components:{
        TableOne
    },
    name: 'EChartsExample',
    setup() {
        const activeTab = ref('first');
        const chartContainer = ref(null);
        const chartContainer2 = ref(null);

        onMounted(() => {
        echarts.use([
            ToolboxComponent,
            TooltipComponent,
            GridComponent,
            LegendComponent,
            BarChart,
            LineChart,
            CanvasRenderer,
            UniversalTransition
        ]);

        const chart = echarts.init(chartContainer.value);
        const chart2 = echarts.init(chartContainer2.value);
        
        const option = {
            tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                color: '#999'
                }
            }
            },
            toolbox: {
            feature: {
                dataView: { show: true, readOnly: false },
                magicType: { show: true, type: ['line', 'bar'] },
                restore: { show: true },
                saveAsImage: { show: true }
            }
            },
            legend: {
            data: ['停车次数', '预期停车次数', '收入']
            },
            xAxis: [
            {
                type: 'category',
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                axisPointer: {
                type: 'shadow'
                }
            }
            ],
            yAxis: [
            {
                type: 'value',
                name: 'times',
                min: 0,
                max: 250,
                interval: 50,
                axisLabel: {
                formatter: '{value} 次'
                }
            },
            {
                type: 'value',
                name: '收入',
                min: 0,
                max: 10000,
                interval: 2000,
                axisLabel: {
                formatter: '{value} 元'
                }
            }
            ],
            series: [
            {
                name: '停车次数',
                type: 'bar',
                tooltip: {
                valueFormatter: function (value) {
                    return value + ' 次';
                }
                },
                data: [
                2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3
                ]
            },
            {
                name: '预期停车次数',
                type: 'bar',
                tooltip: {
                valueFormatter: function (value) {
                    return value + ' 次';
                }
                },
                data: [
                2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3
                ]
            },
            {
                name: '收入',
                type: 'line',
                yAxisIndex: 1,
                tooltip: {
                valueFormatter: function (value) {
                    return value + ' 元';
                }
                },
                data: [
                2100.0, 2000.2, 3000.3, 1000.5, 6000.3, 8900.2, 2089.3, 2893.4, 7890.0, 1600.5, 1200.0, 6000.2
                ]
            }
            ]
        };
        
        const option2 = {
            dataset: {
            source: [
                ['score', '收入', '月份'],
                [89.3, 58212, '1月'],
                [57.1, 78254, '2月'],
                [74.4, 41032, '3月'],
                [50.1, 12755, '4月'],
                [89.7, 20145, '5月'],
                [68.1, 79146, '6月'],
                [19.6, 91852, '7月'],
                [10.6, 101852, '8月'],
                [32.7, 20112, '9月'],
                [32.7, 20112, '10月'],
                [32.7, 20112, '11月'],
                [32.7, 20112, '12月'],
            ]
            },
            grid: { containLabel: true },
            xAxis: { name: '收入(元)' },
            yAxis: { type: 'category' },
            visualMap: {
            orient: 'horizontal',
            left: 'center',
            min: 10,
            max: 100,
            text: ['High Score', 'Low Score'],
            dimension: 0,
            inRange: {
                color: ['#65B581', '#FFCE34', '#FD665F']
            }
            },
            series: [
            {
                type: 'bar',
                encode: {
                x: '收入',
                y: '月份'
                }
            }
            ]
        };

        option && chart.setOption(option);
        option2 && chart2.setOption(option2)
        });

        return {
            chartContainer,
            chartContainer2,
            activeTab
        };
    }
};
</script>
  

<style>

.chart {
    display: flex;
    flex-direction: row;
}

.maintext {
  display: flex;
  justify-content: flex-start;
}


.maintext > .demo-tabs > .el-tabs__content {
  color: #6b778c;
  width: auto;
  height: auto;
  
}

.maintext > .demo-tabs > .el-tabs__header {
  width: auto;
}

.maintext > .demo-tabs {
  margin-right: 0px;
  width: 1300px;
  height: auto;
}

</style>
