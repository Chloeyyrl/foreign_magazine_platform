<template>
    <el-row class="background-image">
      <el-col :span="8"></el-col>
      <el-col :span="8">
        <el-form class="form-container" label-width="80" style="width: 400px;">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input show-password v-model="password"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirm_password">
            <el-input show-password v-model="confirm_password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-link style="margin-right: 10px;" @click="goToLogin">已有帐号？直接登录</el-link>
            <el-button type="warning" plain @click="onRegister">注册</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="8"></el-col>
    </el-row>

</template>

<script>
import { reactive, toRefs } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElForm, ElFormItem, ElInput, ElButton, ElLink, ElMessage } from 'element-plus';

export default {
  components: {
    ElForm,
    ElFormItem,
    ElInput,
    ElButton,
    ElLink
  },

  setup() {
    const router = useRouter(); // 使用 useRouter 获取路由器实例
    const registerForm = reactive({
      username: '',
      password: '',
      confirm_password: ''
    });

    const onRegister = async () => {
      if (registerForm.password !== registerForm.confirm_password) {
        alert("请确认两次输入的密码一致！");
        return;
      }
      // 发送 POST 请求到后端注册API
      try {
        const response = await axios.post('http://localhost:5000/api/register', registerForm);
        if (response.status === 201) {
          ElMessage.success(response.data.message);
          router.push('/'); 
        }  
      } 
      catch (error) {
        console.log(error)
        alert(error.response.data.message); 
      };
    };

    const goToLogin = () => {
      router.push('/');
    };

    // 使用 toRefs 以确保模板中可以直接使用响应式对象的属性
    return {
      ...toRefs(registerForm),
      onRegister,
      goToLogin
    };
  }
};
</script>


<style scoped>
.background-image {
  background-image: url('../assets/background1.png'); /* Adjust the path as necessary */
  background-size: cover; /* Cover the entire area */
  background-position: center center; /* Center the image */
  background-repeat: no-repeat; /* Do not repeat the image */
  height: 100vh; /* Set to the height of the viewport */
  width: 100vw; /* Set to the width of the viewport */
}
/* Overall form styling */
.form-container {
  margin-top: 240px; /* Move form down */
  margin-left: 60px;
  padding: 20px 20px 20px 0;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1); /* subtle shadow */
  background-color: rgba(255, 255, 255, 0.9); /* Adjust opacity here */
  backdrop-filter: blur(500px); 
}

/* Style individual form items */
.el-form-item {
  margin-bottom: 24px; /* space out form items */
}


</style>
