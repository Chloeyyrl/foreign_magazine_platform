<template>
    <el-row class="background-image">
      <el-col :span="8"></el-col>
      <el-col :span="8">
        <el-form class="form-container" label-width="80" style="width: 400px;">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input show-password v-model="registerForm.password"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input show-password v-model="registerForm.confirmPassword"></el-input>
          </el-form-item>
          <el-form-item>
            <el-link style="margin-right: 10px; color:white">已有帐号？直接登录</el-link>
            <el-button type="default" @click="onRegister">注册</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="8"></el-col>
    </el-row>
</template>

<script>
import { reactive, ref } from 'vue';
import axios from 'axios';
import { ElForm, ElFormItem, ElInput, ElButton, ElLink } from 'element-plus';

export default {
  components: {
    ElForm,
    ElFormItem,
    ElInput,
    ElButton,
    ElLink
  },
  setup() {
    const registerForm = reactive({
      username: '',
      password: '',
      confirmPassword: ''
    });

    const onRegister = async () => {
      if (registerForm.password !== registerForm.confirmPassword) {
        alert("请确认两次输入的密码一致！");
        return;
      }
      // 发送 POST 请求到你的后端注册API
      try {
        const response = await axios.post('/api/register', registerForm);
        console.log(response);
        // 根据响应处理成功逻辑，如跳转到登录页面或显示成功消息
      } catch (error) {
        console.error(error);
        // 错误处理，如显示错误消息
      }
    };


    return {
    registerForm,
    onRegister
    };
  }
};
</script>

<style>
.background-image {
  background-image: url('../assets/dim-hou-93AcQpzcASE-unsplash.jpg'); /* Adjust the path as necessary */
  background-size: cover; /* Cover the entire area */
  background-position: center center; /* Center the image */
  background-repeat: no-repeat; /* Do not repeat the image */
  height: 100vh; /* Set to the height of the viewport */
  width: 100vw; /* Set to the width of the viewport */
}
/* Overall form styling */
.form-container {
  margin-top: 150px; /* Move form down */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1); /* subtle shadow */
  background-color: rgba(255, 255, 255, 0.5); /* Adjust opacity here */
  backdrop-filter: blur(50px); 
}

/* Style individual form items */
.el-form-item {
  margin-bottom: 24px; /* space out form items */
}


</style>
