<script setup>
    import Header from '../components/Header.vue';
    import { ref,reactive, onMounted } from 'vue';
    import axios from 'axios';

    const articles = reactive({data:[]});
    const showAll = ref(false);
    const userId = ref('');
    //组件挂载时获取文章数据
    onMounted(() => {
        userId.value = sessionStorage.getItem('userId');
        getArticles();
        });

    const getArticles = () => {
        axios.get('http://localhost:5000/api/get_article')
        .then(response => {
            articles.data = response.data.reverse(); //在使用响应式对象时，直接修改data即可；使用ref时，需要修改value属性值
        })
        .catch(error => {
            console.error('获取文章内容出错：', error);
        });
    };

    // 控制文章显示的计算属性
    const displayedArticles = () => {
        return showAll.value ? articles.data : articles.data.slice(0,4);
    };


    // 切换展示状态的方法
    const toggleShowAll = () => {
        showAll.value = !showAll.value;
    };





</script>

<template>
    <Header/>
    <div class="header-container">
        <h3>外刊广场</h3>
        <el-button v-if="articles.data.length > 4" @click="toggleShowAll" type="primary" plain>
            {{ showAll ? '点击收起' : '展开全部' }}
            <el-icon class="icon-space"><ArrowDown /></el-icon>
        </el-button>
    </div>
    
    <div class="articles-row">
        <div v-for="article in displayedArticles()" :key="article.id" class="article-card-container">
            <el-card class="article-card">
                <div slot="header" class="clearfix">
                    <span>{{ article.title }}</span>
                </div>
                <div class="article-content">
                    <p>{{ article.category }}</p>
                </div>
            </el-card>
        </div>
    </div>
    <h3>我的外刊</h3>

    
    
</template>

<style scoped>
.icon-space {
    margin-left: 4px;
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.articles-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start; /* Or 'space-between' if you want equal spacing */
  margin: -8px; /* Adjust this value based on your gap preference */
}

.article-card-container {
  flex: 0 0 25%; /* This ensures that each card takes up 25% of the container's width */
  max-width: 25%; /* This ensures that each card's maximum width is 25% of the container's width */
  padding: 8px; /* Adjust this value based on your gap preference */
  box-sizing: border-box;
}

.article-card {
  /* Add your styling for the card here */
  width: 100%; /* This ensures the card stretches to fill the container */
  transition: background-color 0.3s; /* 添加平滑过渡效果 */
  background-color:#ecf5ff;
}

.article-card:hover {
  background-color:white; /* 鼠标悬浮时的背景颜色 */
}
</style>