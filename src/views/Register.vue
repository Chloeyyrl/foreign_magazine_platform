<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label for="email">邮箱:</label>
      <input id="email" v-model="form.email" type="email" required>
    </div>
    <div>
      <label for="password">密码:</label>
      <input id="password" v-model="form.password" type="password" required>
    </div>
    <button type="submit">注册</button>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
      }
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axios.post('你的后端API地址/注册', this.form);
        alert('注册成功');
        // 处理成功响应，例如跳转到登录页面或首页
      } catch (error) {
        alert('注册失败');
        // 处理错误响应
      }
    }
  }
}
</script>
