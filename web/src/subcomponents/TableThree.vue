<template>
    <div style="width:auto;padding: 18px;">
        <el-card>
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <el-popover
                :width="300"
                popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;"
                >
                <template #reference>
                    <el-icon><More /></el-icon>
                </template>
                <template #default>
                    <div
                    class="demo-rich-conent"
                    style="display: flex; gap: 16px; flex-direction: column"
                    >
                    <div>
                        <p
                        class="demo-rich-content__name"
                        style="margin: 0; font-weight: 500"
                        >
                        Tip
                        </p>
                        <p
                        class="demo-rich-content__mention"
                        style="margin: 0; font-size: 14px; color: var(--el-color-info)"
                        >
                        @NUAA-CS
                        </p>
                    </div>

                    <p class="demo-rich-content__desc" style="margin: 0">
                        点击下载，以获得更多相关数据
                    </p>
                    </div>
                </template>
                </el-popover>
                <el-button type="danger" round @click="redirectToExternalPage">下载</el-button>
            </div>
        </el-card>
    </div>

    <div>
    <el-row>
        <el-col :sm="16" :xs="32" style="padding: 18px;">
            <el-card>
                <div class="TableT1">
                    <el-table :data="filterTableData" style="width: auto" 
                    :default-sort="{ prop: 'time', order: 'descending' }"
                    class="content1"
                    >
                        <el-table-column label="Time" prop="start_time" sortable width="100" height="auto"></el-table-column>
                        <el-table-column label="Num" prop="id" width="100"></el-table-column>
                        <el-table-column label="End" prop="end_time" width="100"></el-table-column>
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
    </div>
    
</template>

<script>
import { h } from 'vue';
import axios from 'axios';
import { ElNotification } from 'element-plus';
import { getCsrfTokenFromCookies } from '../util.js';

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

            tableData: [],
            isSelected: false,
            
            uploadHeaders: {
                // 在headers中添加X-CSRF字段，使用cookies中的csrf值
                'X-Csrftoken': getCsrfTokenFromCookies(),
            },
        }
    },
    created() {
        axios.get('/api/xxx3/',{
            headers:this.uploadHeaders
        })
        .then(response => {
            // 将获取到的数据赋值给 tableData
            console.log(response.data);
            this.tableData = response.data;
        })
        .catch(error => {
            console.error('获取初始数据失败', error);
        });
        this.caculatemaxcost();
    },
    computed: {
        filterTableData() {
            return this.tableData.filter(data =>
                !this.search || data.id.toLowerCase().includes(this.search.toLowerCase())
            );
        },
        percent() {
            return parseInt((this.usercost / this.maxcost) * 100);
        }
    },
    methods: {
        redirectToExternalPage() {
            // 在这里添加额外的逻辑（可选）
            // 然后浏览器会自动跳转到指定的外部网页

            axios.get('/api/xxx7/',{
                headers: this.uploadHeaders
            })
                .then(response => {
                    const url = response.data;
                    window.location.href = url; // 设置外部网页的 URL
                })
                .catch(error => {
                    console.log(error);
                });

        },

        // eslint-disable-next-line
        handleAsk(index, row) {
            this.load = true;
            setTimeout(() => {
                this.load = false;
                this.username = row.id;
                this.usercost = row.cost;
                this.activities[0].timestamp = row.start_time;
                this.activities[1].timestamp = row.end_time;
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