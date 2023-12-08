<template>
    <div class="cards-container">
        <el-card v-for="index in cardCount" :key="index" class="card" shadow="hover">
        <!-- el-card的内容 -->
        </el-card>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        cardcnt: 3, // 变量的数值大小，这里设定为3
      };
    },
    computed: {
      cardCount() {
        return parseInt(this.cardcnt); // 确保cardCount是一个整数值
      },
    },
  };
</script>
  
<style>
.cards-container {
  display: flex;
  width: 100%;
  flex-wrap:wrap;
  justify-content: space-between;
}


.card {
  width: 200px;
  height: 200px;
  padding: 10px;
}

.card:hover {
    box-shadow: 0 0 20px orange;
}
</style>