<template>
    <el-row>
        <el-col :sm="16" :xs="32" style="padding: 18px;">
            <el-card>
                <div class="TableT1">
                    <el-table :data="filterTableData" style="width: auto" 
                    :default-sort="{ prop: 'time', order: 'descending' }"
                    class="content1"
                    >
                        <el-table-column label="Time" prop="time" sortable width="100" height="auto"></el-table-column>
                        <el-table-column label="Num" prop="num" width="100"></el-table-column>
                        <el-table-column label="End" prop="end" width="100"></el-table-column>
                        <el-table-column label="cost" prop="cost" width="100"></el-table-column>
                        <el-table-column align="right" min-width="70">
                        <template #header>
                            <el-input v-model="search" size="small" placeholder="Type to search"/>
                        </template>
                        <template #default="scope">
                            <el-button
                            size="small"
                            type="danger"
                            @click="handleAsk(scope.$index, scope.row)"
                            >查询</el-button
                            >
                        </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-card>
        </el-col>

        <el-col :sm="8" :xs="16" style="padding: 18px;">
            <el-card v-loading="load">
                <template #header>
                    <div class="UserN">
                        <div style="display: flex;align-items: center;">
                            <el-icon><Avatar /></el-icon>
                            <span>用户</span>
                        </div>
                        <el-button type="success" round >{{username}}</el-button>
                    </div>
                </template>
                <div>
                    <el-timeline class="mytimeline" style="display: block;">
                        <el-timeline-item
                        v-for="(activity, index) in activities"
                        :key="index"
                        :timestamp="activity.timestamp"
                        class="my-timeline-item"
                        >
                        {{ activity.content }}
                        </el-timeline-item>
                    </el-timeline>
                </div>
                <div style="display: flex; justify-content: space-between;align-items: center;">
                    <el-progress
                        :text-inside="true"
                        :stroke-width="20"
                        :percentage="percent"
                        status="exception"
                        :style="{ width: '80%' }"
                    />
                    <span>{{ usercost }}(元)</span>
                </div>
            </el-card>
        </el-col>

    </el-row>
    
</template>

<script>
import { h } from 'vue'
import { ElNotification } from 'element-plus'

export default {
    data() {
        return {
            load: false,
            username: '',
            usercost: 0,
            maxcost: 100,
            search: '',

            activities:[
                {
                    content:'start',
                    timestamp:'12:01'
                },
                {
                    content:'end',
                    timestamp:'12:01'
                }
            ],

            tableData: [
                {
                    time: '12:01',
                    num: 'NU234451',
                    end: '12:02',
                    cost: '100'
                },
                {
                    time: '12:22',
                    num: 'NU234411',
                    end: '12:52',
                    cost: '60'
                },
                {
                    time: '12:41',
                    num: 'NU232351',
                    end: '12:52',
                    cost: '68'
                },
                {
                    time: '01:01',
                    num: 'NU223451',
                    end: '12:52',
                    cost: '90'
                },
            ],
            isSelected: false,

        }
    },
    created() {
        this.caculatemaxcost();
    },
    computed: {
        filterTableData() {
            return this.tableData.filter(data =>
                !this.search || data.num.toLowerCase().includes(this.search.toLowerCase())
            );
        },
        percent() {
            return parseInt((this.usercost / this.maxcost) * 100);
        }
    },
    methods: {
        // eslint-disable-next-line
        handleAsk(index, row) {
            this.load = true;
            setTimeout(() => {
                this.load = false;
                this.username = row.num;
                this.usercost = row.cost;
                this.activities[0].timestamp = row.time;
                this.activities[1].timestamp = row.end;
                ElNotification({
                    title: 'Tip',
                    message: h('i', { style: 'color: teal' }, '加载完毕')
                })
            }, 2000);
            
        },

        caculatemaxcost() {
            let max = 0;
            for (let i = 0;i < this.tableData.length;i ++ ) {
                const cost = parseInt(this.tableData[i].cost);
                if(cost > max) {
                    max = cost;
                }
            }
            if(max === 0) {
                max = 1;
            }
            this.maxcost = max;
        }
        
    },
};
</script>
  
<style scoped>

.is-selected {
  color: #1989fa;
}

.TableT1 {
    width: 800px;
}

.content1{
    caret-color: transparent;
    width: 100%; overflow: auto;
}

.UserN {
    display: flex;
    justify-content: space-between;
    align-items: center;
}


:deep() .mytimeline .my-timeline-item .el-timeline-item__wrapper {
  width: 30%;
}

</style>