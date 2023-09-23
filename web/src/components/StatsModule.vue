<template>
    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="date" label="Date" width="180" />
      <el-table-column prop="name" label="Name" width="180" />
      <el-table-column prop="time" label="Time" />
    </el-table>
</template>

<script>
export default {
    name: "DaTa",
    data(){
        return {
            tableData : [
                {
                    date: '2023-09-20',
                    name: 'SN893112',
                    time: '1h',
                },
                {
                    date: '2023-09-20',
                    name: 'SN893112',
                    time: '1h',
                },
                {
                    date: '2023-09-20',
                    name: 'SN893112',
                    time: '1h',
                },
                {
                    date: '2023-09-20',
                    name: 'SN893112',
                    time: '1h',
                },
            ]
        }
    }
}
</script>