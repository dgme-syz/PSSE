<template>
    <el-table
      :data="tableData"
      :default-sort="{ prop: 'date', order: 'descending' }"
      style="width: 100%; overflow: auto;"
    >
      <el-table-column prop="date" label="日期" sortable width="180" />
      <el-table-column prop="state" label="状态" width="180" />
      <el-table-column prop="income" label="收入(元)" :formatter="formatter" sortable :sort-method="sortMethod" min-width="180"/>
    </el-table>
  </template>
  
  <script>
  import axios from 'axios';
  import { getCsrfTokenFromCookies } from '../util.js';

  export default {
    data() {
      return {
        tableData: [],
        uploadHeaders: {
          // 在headers中添加X-CSRF字段，使用cookies中的csrf值
          'X-Csrftoken': getCsrfTokenFromCookies(),
        },
      };
    },
    mounted() {
    // 在 mounted 钩子中初始化 tableData
      this.GetFormMonth();
    },
    methods: {

      GetFormMonth() {
        const currentDate = new Date(); // 获取当前日期
        const startOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1); // 本月月初
        const endOfDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()); // 当前日期

        // 格式化日期为 'YYYY-MM-DD' 格式
        const formatDateString = date => {
          const year = date.getFullYear();
          const month = (date.getMonth() + 1).toString().padStart(2, '0');
          const day = date.getDate().toString().padStart(2, '0');
          return `${year}-${month}-${day}`;
        };

        // 构建要发送的数据对象
        const data = {
          start_time: formatDateString(startOfMonth),
          end_time: formatDateString(endOfDay)
        };

        // 发送POST请求
        axios.post('/api/xxx1/', data, {
          headers:this.uploadHeaders
        })
          .then((response) => {
            console.log('POST请求成功', response);
            this.tableData = response.data;
          })
          .catch((error) => {
            console.error('POST请求失败', error);
          });

      },

      // eslint-disable-next-line
      formatter(row, column) {
        return row.income;
      },
      sortMethod(a, b) {
        const numberA = parseFloat(a.income)
        const numberB = parseFloat(b.income)
        if (numberA < numberB) {
            return -1
        }
        if (numberA > numberB) {
            return 1
        }
        return 0
        },
    },
  };
  </script>
  