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
            <el-table-column prop="licensePlate" label="车牌号码"></el-table-column>
            <el-table-column prop="parkingTime" label="开始时间"></el-table-column>
            <el-table-column prop="endtime" label="结束时间"></el-table-column>
            <el-table-column prop="carType" label="车辆类型"></el-table-column>
            </el-table>
        </el-card>
    </div>
</template>

<script>

import { h } from 'vue';
import { ElNotification } from 'element-plus';

export default {
data() {
    return {
        carList: [],        // 当前场内车辆数据
        loading: false,     // 加载状态
        searchText: '',     // 搜索框的内容
    };
},
computed: {
    filteredCarList() {
    // 根据搜索框的内容过滤车辆数据
    if (this.searchText) {
        const keyword = this.searchText.toLowerCase();
        return this.carList.filter(car =>
        car.licensePlate.toLowerCase().includes(keyword) ||
        car.parkingTime.includes(keyword) ||
        car.carType.toLowerCase().includes(keyword) ||
        car.endtime.toLowerCase().includes(keyword)
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
        { licensePlate: '京A12345', parkingTime: '10:00', carType: '小型车', endtime: '10:55' },
        { licensePlate: '京B67890', parkingTime: '10:15', carType: '大型车', endtime: '10:55' },
        { licensePlate: '京C24680', parkingTime: '10:30', carType: '小型车', endtime: '10:55' },
        { licensePlate: '京D13579', parkingTime: '10:45', carType: '摩托车', endtime: '10:55' }
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

        // 模拟异步请求，假设请求耗时为2秒
        setTimeout(() => {
            this.loading = false;

            ElNotification({
                title: 'Tip',
                message: h('i', {style:'color: teal'},'更新完毕')                
            })


        }, 2000);
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