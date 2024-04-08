<template>
    <el-row class="background-image">
      <el-col :span="8"></el-col>
      <el-col :span="8">
        <el-form class="form-container" label-width="80" style="width: 400px;">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input show-password v-model="loginForm.password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-link style="margin-right: 10px; color:white" @click="goToRigister">没有帐号？立即注册</el-link>
            <el-button type="default" @click="onLogin">登录</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="8"></el-col>
    </el-row>
</template>

<script>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
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
    const router = useRouter();
    const loginForm = reactive({
      username: '',
      password: ''
    });

    const onLogin = async () => {
      if (!loginForm.username || !loginForm.password) {
        alert("请填写用户名和密码！");
        return;
      }

      try {
        const response = await axios.post('/api/login', {
          username: loginForm.username,
          password: loginForm.password
        });
        
        if (response.data) {
          router.push('/main');
        } 
      } 
      catch (error) {
        alert(error.response.data.message);
      }
    };

    const goToRigister = () => {
      router.push('/register');
    };

    return {
    loginForm,
    onLogin,
    goToRigister
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
