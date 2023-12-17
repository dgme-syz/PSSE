<template>
    <div style="width: 30%;height: auto;">
        <el-card class="box-card" style="width: 100%;height: 100%;" v-loading="load">
            <template #header>
                <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                <h3 class="w2">A</h3>
                <p>自动寻路</p>
                </div>
            </template>
            <div style="display: flex !important; align-items: flex-start !important; justify-content: flex-start !important;">
                <span style="color: gray;">基于dijkstra算法给出当前入口最近空车位导航结果</span>
            </div>
            <div class="enter_choice">
                <el-row>
                    <h3 class="w1">入口选择</h3>
                </el-row>
                <el-row>
                    <el-select  
                    v-model="value"
                    placeholder="Select"
                    style="width: auto"
                    >
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    /></el-select>
                </el-row>
            </div>
            <div>
                <el-row>
                    <h3 class="w1">车位状态</h3>
                </el-row>
                <el-row>
                    <div style="display: flex !important;align-items: center;justify-content: space-between;width:100%">
                        <div style="width:50%">
                            <div style="display: flex;align-items: center;">
                            <el-icon style="margin-left:25%;"><StarFilled /></el-icon>
                            <el-tooltip content="剩余空车位数量" placement="top">
                            <span class="w1">车位数量</span>
                            </el-tooltip>
                            </div>
                        </div>
                        <div style="width:50%;margin-right:25%"><span class="w1">{{ counts }}</span></div>
                    </div>
                </el-row>
                <el-row>
                    <div style="display: flex !important;align-items: center;justify-content: space-between;width:100%;margin-top:3%">
                        <div style="width:50%">
                            <div style="display: flex;align-items: center;">
                            <el-icon style="margin-left:25%;"><StarFilled /></el-icon>
                            <el-tooltip content="距离空车位最短的距离" placement="top">
                            <span class="w1">最短距离</span>
                            </el-tooltip>
                            </div>
                        </div>
                        <div style="width:50%;margin-right:25%"><span class="w1">{{ distance }}</span></div>
                    </div>
                </el-row>
            </div>

            <div class="button"> 
                <el-button color="#626aef" :dark="isDark" @click="submitUpload">更新车位</el-button>
                <el-button color="#626aef" :dark="isDark" @click="askforinfo">自动寻路</el-button>
            </div>
        </el-card>
  </div>
  <div style="width: 30%;height: auto;margin-left: auto;">
    <el-card class="left_box" style="height: 100%;">
        <template #header>
            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <h3 class="w2">B</h3>
            <p>更新车位</p>
            </div>
        </template>
        <div style="display: flex !important; align-items: flex-start !important; justify-content: flex-start !important;">
            <span style="color: gray;">上传传感器最新的拍摄图片，以更新节点信息</span>
        </div>
        <div >
            <el-row>
                <h3 class="w1">遥感图片</h3>
            </el-row>
            <el-upload class="upload-demo" drag action="api/nodeupdate/" :on-success="handleUploadSuccess" 
            :headers= uploadHeaders :auto-upload="false" ref="uploadRef"
            name="image"
            multiple >
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
        </div>
    </el-card>
  </div>
  <div style="width: 30%;height: auto;margin-left: auto;">
    <el-card style="height: 100%;">
        <template #header>
            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <h3 class="w2">C</h3>
            <p>输出路径</p>
            </div>
        </template>
        <div style="display: flex !important; align-items: flex-start !important; justify-content: flex-start !important;">
            <span style="color: gray;">输出最短路径路线</span>
        </div>
        <!-- 返回服务器传来的图片 -->
        <el-row><h3 class="w1">路线规划</h3></el-row>
        <div style="height: 30vh;">
            <el-image :src="imageURL" class="img"></el-image>
        </div>
    </el-card>
  </div>
</template>

<script>
import { h, ref } from 'vue';
import axios from 'axios';
import { getCsrfTokenFromCookies } from '../util.js';
import { UploadFilled } from '@element-plus/icons-vue';
import { ElNotification } from 'element-plus';
export default {
    data() {
        return {
            value: [],
            load: false,
            counts: 10, 
            distance: 100,
            options: [
                {
                    value: '0',
                    label: '左入口',
                },
                {
                    value: '1',
                    label: '右入口',
                },
            ],
            uploadHeaders: {
                // 在headers中添加X-CSRF字段，使用cookies中的csrf值
                'X-Csrftoken': getCsrfTokenFromCookies(),
            },
            imageURL: null,
        };
    },

    methods: {
        handleUploadSuccess(response) {
            // 上传图片更新信息
            if(response.success) {
                ElNotification({
                    title: 'Tip',
                    message: h('i', {style:'color: teal'},'成功更新当前车位信息')                
                })
            } else {
                ElNotification({
                    title: 'Tip',
                    message: h('i', {style:'color: teal'},'更新失败:(')                
                })
            }
        },
        askforinfo() {
            this.load = true
            axios.post('/api/outputpath/', {type: this.value.length ? this.value : '0'}, {
                headers: this.uploadHeaders,
            }).then((response) => {
                this.distance = response.data.dis
                this.imageURL = response.data.url
                setTimeout(() => {
                    this.load = false
                }, 500)
            }).catch((error) => {
                console.log(error)
                console.log({type: this.value.length ? this.value : '0'})
                setTimeout(() => {
                    this.load = false
                }, 500)
            })
        }
    }, 

    components: {
        UploadFilled // 注册图标组件
    },

    setup() {
        const uploadRef = ref(null);
        const submitUpload = () => {
            uploadRef.value.submit();
        };
        return { uploadRef, submitUpload };
    },

    mounted() {
        this.uploadRef = this.$refs.uploadRef;
    },
};

</script>

<style>
.enter_choice {
    display: flex !important; 
    flex-direction: column;
}
.button {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.w1:hover {
    color:#FF6F61
}
.w2:hover {
    color: #7FC7E2;
}
.upload-demo {
    margin-top: 5%;
}
.img {
    width: 100%;
    height: 100%;
    
}
</style>