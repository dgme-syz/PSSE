<template>
  <div>
    <form @submit.prevent="registerUser">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" required />

      <label for="password">Password:</label>
      <input
        type="password"
        id="password"
        v-model="password"
        required
      />

      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'; // 引入Axios

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    registerUser() {
      // 获取Django生成的CSRF令牌并包含在Axios请求头中
      axios.defaults.xsrfCookieName = 'csrftoken'; // Django默认的CSRF cookie名称
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'; // Django默认的CSRF请求头名称

      const userData = {
        username: this.username,
        password: this.password,
      };

      axios
        .post('/api/register/', userData) // 发送POST请求到Django的/api/register/端点
        .then((response) => {
          // 处理成功响应，可能会有一些反馈或跳转到登录页面
          console.log('Registration successful');
          this.$router.push('/login'); // 示例：重定向到登录页面
        })
        .catch((error) => {
          // 处理错误响应，可能显示错误消息
          console.error('Registration failed:', error);
        });
    },
  },
};
</script>
