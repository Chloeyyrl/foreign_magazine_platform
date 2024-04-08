<script setup>
import axios from 'axios';
import { reactive, onMounted } from 'vue';

const userInfo = reactive({
  username: '',
  userid: ''
});

const fetchUserInfo = async () => {
  try {
    // 使用axios发起GET请求
    console.log('正在请求:', '/api/user');
    const response = await axios.get('http://localhost:5000/api/user');
    console.log(response)
    // 直接从response中解构出data，axios会自动处理JSON解析
    // const { data } = response;
    
    // if (response.status == 200) {
    //   // 假设后端返回的数据包含username和userid字段
    //   userInfo.username = data.username;
    //   userInfo.userid = data.userid;
    // } else {
    //   console.error('用户未登录或获取用户信息失败');
    //   // 清除已有的用户信息
    //   userInfo.username = null;
    //   userInfo.userid = null;
    // }
  } catch (error) {
    console.error('请求错误', error);
    // 出现请求错误时，清除已有的用户信息
    userInfo.username = null;
    userInfo.userid = null;
  }
};

onMounted(() => {
  fetchUserInfo();
});

</script>

<template>
  <el-container>
    <el-header>
      <el-menu class="el-menu-demo" mode="horizontal">
        <el-menu-item index="1">
            <el-icon><house /></el-icon>
            用户名：{{ userInfo.username }}
        </el-menu-item>

        <div class="menu-spacer"></div>

        <el-menu-item index="2">
            <el-icon><switch-button /></el-icon>
        </el-menu-item>
      </el-menu>
    </el-header>
  </el-container>

</template>


<style scoped>



</style>