<script>

import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const userName = ref('');
    const userId = ref('');
    const router = useRouter();

    onMounted(() => {
      userName.value = sessionStorage.getItem('userName');
      userId.value = sessionStorage.getItem('userId');
    });

    // 定义退出函数
    const logout = () => {
      sessionStorage.removeItem('userName');
      sessionStorage.removeItem('userId');
      router.push('/');
    };

    return {
      userName,
      userId,
      logout,
    };
  },
};

</script>

<template>
    <!-- <el-header> -->
      <el-menu class="el-menu-demo" mode="horizontal" style="display: flex; justify-content: space-between;">
        <el-menu-item index="1">
            <el-icon><house /></el-icon>
            <b>{{ userName }}</b>
        </el-menu-item>
        <div class="menu-spacer"></div>
        <el-menu-item index="2" @click="logout">
            <el-icon><switch-button /></el-icon>
        </el-menu-item>
      </el-menu>
    <!-- </el-header> -->
  

</template>


<style scoped>



</style>