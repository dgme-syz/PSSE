<template>
  <div id="pic">
      <el-card class="mainbox">
        <el-row class="row" :gutter="40">
          <!-- 使用el-card包裹上传窗口 -->
          <!-- 上传车辆图片 -->
          <el-col class="lcol" :sm="12" :xs="24">
            <el-card class="left_box">
              <el-upload class="upload-demo" drag action="api/pic/" :on-success="handleUploadSuccess" multiple >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  Drop file here or <em>click to upload</em>
                </div>
                <template #tip>
                  <div class="img_info_1" style="border-radius: 0 0 5px 5px">
                    <span style="color: white; letter-spacing: 6px">进入车辆图片</span>
                  </div>
                </template>
              </el-upload>
            </el-card>
          </el-col>

          <el-col class="rcol" :sm="12" :xs="24">
            <el-card class="right_box">
              <!-- 返回服务器传来的图片 -->
              <el-image :src="imageURL" @error="handleError" class="img">
                
              </el-image>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
  </div>
  <div id="data">

    <el-card class = "stats">
      <div class="subdata">
        <el-col>
          <el-statistic :value="38">
            <template #title>
              <div style="display: inline-flex; align-items: center">
                空车位
              </div>
            </template>
            <template #suffix>/100</template>
          </el-statistic>
        </el-col>
      </div>
      <div class="subdata">
        <el-col>
          <el-statistic  :value="10" >
          <template #title>
              <div style="display: inline-flex; align-items: center">
                过去1h收入(元)
              </div>
              <el-icon><Coin /></el-icon> 
            </template>
          </el-statistic>
        </el-col>
      </div>

      <div class="subdata">
        <el-col>
          <el-statistic  :value="1120" >
          <template #title>
              <div style="display: inline-flex; align-items: center">
                过去1天收入(元)
              </div>
              <el-icon><Coin /></el-icon> 
            </template>
          </el-statistic>
        </el-col>
      </div>

      <div class="subdata">
        <el-col>
          <el-statistic  :value="199020" >
          <template #title>
              <div style="display: inline-flex; align-items: center">
                过去1月收入(元)
              </div>
              <el-icon><Coin /></el-icon> 
            </template>
          </el-statistic>
        </el-col>
      </div>

    </el-card>
  </div>




</template>
  
<script>
import { defineComponent } from 'vue';
import { UploadFilled } from '@element-plus/icons-vue';


export default defineComponent({
  name: 'App',

  data() {
    return {
      imageURL:null
    }
  },

  components: {
      UploadFilled // 注册图标组件
  },

  // 组件逻辑
  
  methods: {
    handleUploadSuccess(response) {
      // 处理上传成功后的回调
      console.log(response);
      console.log('ok');
    },
  },
});
</script>

<style scoped>


#pic {
  padding: 50px;
  height: 500px;
}

#data {
  padding: 50px;
  height: 500px;
}

.mainbox {
  width: 970px;
  height: 450px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.row {
  display: flex;
  justify-content: center;
  align-items: center;
}

.lcol {
  height: 100%;
  width: 100%;
}

.rcol {
  height: 100%;
  width: 100%;
}

@media (max-width: 768px) { /* 假设移动端宽度为768px */
  .lcol,
  .rcol {
    height: 30%;
  }
}

.right_box {
  max-width: 100%;
  height: 100%;
  margin-left: 30px;
}

.left_box {
  max-width: 100%;
  height: 100%;
  margin-right: 30px;
}

.img {
  width: 300px;
  height: 262px;
}

.upload-demo {
  width: 300px;
  height: 262px;
  align-items: center;
}

/deep/ .upload-demo .el-upload-dragger {
  width: 100% !important;
  height: 220px !important;
}

.img_info_1 {
  height: 30px;
  width: 300px;
  text-align: center;
  background-color: #ac8daf;
  line-height: 30px;
}

.subdata {
  padding: 10px;
}

.stats {
  height: 450px;
}

</style>