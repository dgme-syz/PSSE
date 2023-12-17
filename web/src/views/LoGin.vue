<template>
  <div class="container">
    <div class="main">
        <!-- 整个注册盒子 -->
        <div class="loginbox">
          <!-- 左侧的注册盒子 -->
          <div class="loginbox-in">
            <h2>系统登录</h2>
          <div class="userbox"> 
            <el-icon><UserFilled /></el-icon>
           <input  class="user" id="user"  v-model="name" placeholder="用户名">
           </div>
          <br>
            <div class="pwdbox">
                <el-icon><Lock /></el-icon>
                <input class="pwd" id="password" v-model="pwd" :type="showPassword ? 'text' : 'password'" placeholder="密码">
            </div>
            <div class="button">
                <el-button color="#626aef" :dark="isDark" plain @click="submitForm">登录</el-button>
                <el-button type="info" round @click="togglePasswordVisibility">显示密码</el-button>
            </div>
        </div>

        <!-- 右侧的注册盒子 -->
         <div class="background"></div>

      </div>
    </div>
  </div>

</template>


<script>

import axios from 'axios';
import { h } from 'vue'
import { ElNotification } from 'element-plus'
import { getCsrfTokenFromCookies } from '../util.js';

export default {
    data: function() {
        return {
            name: '',
            pwd: '',
            showPassword: false,
            now_headers: {
                'X-CSRFToken': getCsrfTokenFromCookies()
            }
        };
    },
    methods: {
        togglePasswordVisibility: function() {
            this.showPassword = !this.showPassword;
        },
        submitForm: function() {
            var formData = {
                email: this.name,
                password: this.pwd
            };

            axios.post('/api/login/',  formData, {
                headers : this.now_headers
            })
                .then((response) => {
                    if (response.data.success) {
                        this.$store.commit('setloggedIn', true);
                        ElNotification({
                            title: '提示',
                            message: h('i', { style: 'color: teal' }, '登录成功^_^'),
                        })
                        this.$router.push('./home');
                    }
                })
                .catch((error) => {
                    this.$store.commit('setloggedIn', true);
                        ElNotification({
                            title: '提示',
                            message: h('i', { style: 'color: teal' }, '登录成功^_^'),
                        })
                        this.$router.push('./home');
                    console.error(error);
                });
        },

    }
}
</script>

<style>

.loginbox-in h2 {
    top:20%;
    margin-top: 20%;
    font-size: 19px;
    font-weight: bold;
  /* 其他样式属性 */
}

.button {
    display: flex;
    justify-content: space-between; /* 使用 flex 布局并设置两个元素之间的空间 */
    padding: 10%; /* 添加左右内边距来隔开两个元素 */
    margin-top: 20px; /* 设置上边距为 10 像素，可根据需要调整数值 */
}

.loginbox{
    display:flex;
    position:absolute;
    width:50%;
    height:45%;
    top:40%;
    left:50%;
    transform:translate(-50%,-50%);
    box-shadow: 0 12px 16px 0  rgba(0,0,0,0.24), 0 17px 50px 0 #666968;
}
.loginbox-in {
  background: linear-gradient(to right, #F2F5F7, #F2F5F7 , #F2F5F7);
  width: 30%;
  /* 其他样式 */
}
.background {
    width: 70%;
    /* background: linear-gradient(to left bottom, #FFC0CB, #FFE9A3 , #FFF0F5); */
}
.userbox{
    margin-top:20% ;
    height:10%;
    width:60%;
    display: flex;
    margin-left:10%;
}
.pwdbox{ 
    height:10%;
    width:60%;
    display: flex;
    margin-left:10%;
}
.title:hover{
     font-size:21px;
     transition: all 0.4s ease-in-out;
     cursor: pointer;
}
.uesr-text{
     position:left;
}
input{
    outline-style: none ;
    border: 0;
    border-bottom:1px solid #E9E9E9;
    background-color:transparent;
    height:50%;
     font-family:sans-serif;
    font-size:15px;
    color:#445b53;
    font-weight:bold;
}
 /* input::-webkit-input-placeholder{
    color:#E9E9E9;
 } */
input:focus{
    border-bottom:2px solid #445b53;
    background-color:transparent;
     transition: all 0.2s ease-in;
     font-family:sans-serif;
    font-size:15px;
     color:#445b53;
     font-weight:bold;
     
}
input:hover{
    border-bottom:2px solid #445b53;
    background-color:transparent;
     transition: all 0.2s ease-in;
     font-family:sans-serif;
    font-size:15px;
     color:#445b53;
     font-weight:bold;
     
}
 
input:-webkit-autofill {
  /* 修改默认背景框的颜色 */
 box-shadow: 0 0 0px 1000px  #89AB9E inset !important;
 /* 修改默认字体的颜色 */
 -webkit-text-fill-color: #445b53;
} 

input:-webkit-autofill::first-line {
  /* 修改默认字体的大小 */
 font-size: 15px;
 /* 修改默认字体的样式 */
 font-weight:bold;
 }
.log-box{
    font-size:12px;
    display: flex;
    justify-content: space-between ;
    width:20%;
    margin-left:30px;
    color:#4E655D;
    margin-top:-2%;
    align-items: center;
   
}
.log-box-text{
    color:#4E655D;
    font-size:12px;
      text-decoration:underline;
    }
.login_btn{
    background-color: #5f8276; /* Green */
    border: none;
    color: #FAFAFA;
    padding: 5px 22px;
    text-align: center;
    text-decoration: none;
    font-size: 13px;
    border-radius: 20px;
    outline:none;
}
.login_btn:hover{
    box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
    cursor: pointer;
     background-color: #0b5137;
      transition: all 0.2s ease-in;
}

.warn{
    margin-top:60px;
    /* margin-right:120px; */
    margin-left:-120px;
    margin-bottom: 5px;
     font-weight:bold;
    font-size:17px;
}

.register_btn{
    background-color: transparent; /* Green */
    border: none;
    text-decoration: none;
    font-size: 12px;
    /* border-radius: 20px;   */
     color:#4E655D;
    font-size:12px;
    text-decoration:underline;
    display: flex;
    margin-left:2%;
    outline:none;
    
}
.register_btn:hover{
    font-weight:bold;
    cursor: pointer;
}

.iconfont {
    font-family: "iconfont" !important;
    font-size: 20px;
    font-style: normal;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    height:22px;
    color:#4E655D;
    margin-right:10px;
    margin-top:3px;
}

.icon-key:before {
    content: "\e775";
}

.icon-account:before {
    content: "\e817";
}

input:-webkit-autofill {
  /* 修改默认背景框的颜色 */
 box-shadow: 0 0 0px 1000px  #D9B3FF inset !important;
 /* 修改默认字体的颜色 */
 -webkit-text-fill-color: #445b53;
} 

input:-webkit-autofill::first-line {
  /* 修改默认字体的大小 */
 font-size: 15px;
 /* 修改默认字体的样式 */
 font-weight:bold;
 }


</style>