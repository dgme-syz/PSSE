<template>
  <!-- 由于 content 单独存在，所以直接初始化所有样式 -->
  <!-- 注意这里会带来的潜在问题 -->
  <div style="all: initial;width: auto;">
    <el-dialog v-model="visible" :show-close="false">
      <template #header="{ close, titleId, titleClass }">
        <div class="my-header" style="display:flex;justify-content:space-between;align-items: center;">
          <h4 :id="titleId" :class="titleClass">步骤</h4>
          <el-button type="danger" @click="close">
            <el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
            Close
          </el-button>
        </div>
      </template>
      <div style="align-items: center;display: flex;justify-content: center;">
        <el-steps :active="num" style="width: fit-content;" >
          <el-step title="Step 1" description="手动或者通过摄像头上传车辆图片" />
          <el-step title="Step 2" description="点击Upload上传图片至服务端" />
          <el-step title="Step 3" description="web接收服务器传来的结果，并更新数据" />
          <el-step title="Step 4" description="success" />
        </el-steps>
      </div>
      <div style="justify-content: flex-end;display: flex;">
        <el-button type="primary" style="margin-right: 20px;margin-top: 30px;"  @click="safe_subtract">Prev</el-button>
        <el-button type="primary" style="margin-right: 30px;margin-top: 30px;"  @click="safe_add">Next</el-button>
      </div>
    </el-dialog>
  </div>


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
        <div style="margin-top: 20px;">
          <el-button type="primary">
            Upload<el-icon class="el-icon-right1"><Upload /></el-icon>
          </el-button>
          <el-button type="primary" @click="updateask">Update</el-button>
          <el-button type="primary" @click="visible = true">
            help<el-icon><QuestionFilled /></el-icon>
          </el-button>
        </div>
      </el-card>
  </div>
  <div id="data">

    <el-card class = "stats" v-loading="loadenter">
      <div class="subdata">
        <el-col>
          <el-statistic :value="this.$store.state.EmptyCarPostion">
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
          <el-statistic  :value="this.$store.state.BeforeOneHourIncome" >
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
          <el-statistic  :value="this.$store.state.BeforeOneDayIncome" >
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
          <el-statistic  :value="this.$store.state.BeforeOneMonthIncome" >
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
import { defineComponent , h} from 'vue';
import { UploadFilled } from '@element-plus/icons-vue';
import { Upload } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus';

export default defineComponent({
  name: 'App',

  data() {
    return {
      imageURL: null,
      Upload,
      visible: false,
      num: 1,
      loadenter:false,
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
    safe_add(){
      this.num = this.num + 1;
      if(this.num > 4) this.num = 4; 
    },
    safe_subtract(){
      if(this.num > 0) 
        this.num = this.num - 1;
    },
    updateask() {
      this.loadenter = true,
      setTimeout(() => {
          this.loadenter = false;
          
          // 模拟获取表单
          var form = {
            ECP : 12,
            BOHI : 1122,
            BODI : 1233,
            BOMI : 114514, 
          }

          this.$store.commit("setIncomInfo",form);

          ElNotification({
              title: 'Tip',
              message: h('i', {style:'color: teal'},'更新完毕')                
          })
      }, 2000);
    }
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

:deep() .upload-demo .el-upload-dragger {
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

.my-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

</style>