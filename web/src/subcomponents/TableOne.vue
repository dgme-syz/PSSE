<template>
    <el-table
      :data="tableData"
      :default-sort="{ prop: 'date', order: 'descending' }"
      style="width: 100%; overflow: auto;"
    >
      <el-table-column prop="date" label="日期" sortable width="180" />
      <el-table-column prop="name" label="状态" width="180" />
      <el-table-column prop="income" label="收入(元)" :formatter="formatter" sortable :sort-method="sortMethod" min-width="180"/>
    </el-table>
  </template>
  
  <script>
  export default {
    data() {
      return {
        tableData: [
          {
            date: '2023-10-01',
            name: '差',
            income: '1119',
          },
          {
            date: '2023-10-02',
            name: '良',
            income: '1233',
          },
          {
            date: '2023-10-03',
            name: '良',
            income: '1233',
          },
          {
            date: '2023-10-04',
            name: '优',
            income: '13192',
          },
          {
            date: '2023-10-05',
            name: '优',
            income: '312',
          },
          {
            date: '2023-10-06',
            name: '优',
            income: '1312123',
          },
          {
            date: '2023-10-07',
            name: '优',
            income: '13112',
          },
        ],
      };
    },
    methods: {
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
  