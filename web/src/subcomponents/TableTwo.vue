<template>
    <div style="margin-bottom: 2%;">
        <el-card style="caret-color: transparent;">
        <!-- 搜索框 -->
        <div class="search_and_update">
            <div style="display: flex;align-items: center;width: auto;">
                <el-icon style="margin-right: 10px;"><Search /></el-icon>
                <el-input v-model="searchText" placeholder="请输入要搜索的内容" @input="handleSearch" style="width:auto"></el-input>
            </div>
            <el-button type="primary" round class="update_part" @click="handleUpdate">update</el-button>
        </div>

        </el-card>
    </div>
    <div>
        <el-card style="width: auto;">
            <el-table :data="filteredCarList" style="width: 100%" v-loading="loading" class="Table34" >
            <el-table-column prop="id" label="车牌号码"></el-table-column>
            <el-table-column prop="start_time" label="开始时间"></el-table-column>
            <el-table-column prop="end_time" label="结束时间"></el-table-column>
            </el-table>
        </el-card>
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
        carList: [],        // 当前场内车辆数据
        loading: false,     // 加载状态
        searchText: '',     // 搜索框的内容
        uploadHeaders: {
        // 在headers中添加X-CSRF字段，使用cookies中的csrf值
        'X-Csrftoken': getCsrfTokenFromCookies(),
      },
    };
},
computed: {
    filteredCarList() {
    // 根据搜索框的内容过滤车辆数据
    if (this.searchText) {
        const keyword = this.searchText.toLowerCase();
        return this.carList.filter(car =>
        car.id.toLowerCase().includes(keyword) ||
        car.start_time.includes(keyword) ||
        car.endt_ime.toLowerCase().includes(keyword)
        );
    } else {
        return this.carList;
    }
    }
},
mounted() {
    this.loading = true; // 开始加载数据
    // 模拟异步获取数据
    setTimeout(() => {
    this.carList = [
        { id: '京A12345', start_time: '10:00', end_time: '10:55' },
        { id: '京B67890', start_time: '10:15', end_time: '10:55' },
        { id: '京C24680', start_time: '10:30', end_time: '10:55' },
        { id: '京D13579', start_time: '10:45', end_time: '10:55' }
    ];
    this.loading = false; // 数据加载完成
    }, 1000);
},
methods: {
    handleSearch() {
    // 处理搜索框输入事件
    // 在这里可以触发搜索操作，例如发送网络请求获取匹配的数据
    // 这里只是一个示例，没有实际发送网络请求
    console.log('搜索框内容:', this.searchText);
    },
    handleUpdate() {
        this.loading = true;

        axios.get('/api/xxx2/',{
            headers:this.uploadHeaders
        })
          .then(response => {
            // 在这里处理从服务器获取的数据
            console.log('从服务器获取的数据', response.data);
            this.loading = false;
            
            this.carList = response.data;
            ElNotification({
                title: 'Tip',
                message: h('i', {style:'color: teal'},'更新完毕')                
            })
          })
          .catch(error => {
            console.error('获取数据失败', error);
            ElNotification({
                title: 'Warning',
                message: h('i', {style:'color: teal'},'更新失败')                
            })
            this.loading = false;
          });

    },
}
};
</script>

<style>


.search_and_update {
    display: flex;
    justify-content: space-between;
}

</style>