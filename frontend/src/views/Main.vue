<script setup>
import Header from '../components/Header.vue';
import { ref, reactive, onMounted} from 'vue';
import { useRouter } from 'vue-router';

import axios from 'axios';

const articles = reactive({ data: [] });
const showAll = ref(false);
const userId = ref('');
const router = useRouter(); // 使用路由

// 组件挂载时获取文章数据
onMounted(() => {
    userId.value = sessionStorage.getItem('userId');
    getArticles();
});

// 跳转到文章详情页
const navigateToArticle = (articleId) => {
    router.push({
        name: 'Read',
        params: { id: articleId }
    }).catch(error => {
        console.error('Routing error:', error);
    });
};

const checkReadingStatus = (article) => {
    axios.get('http://localhost:5000/api/check_reading_status', {
        params: {
            userId: userId.value,
            article_id: article.id,
        }
    })
    .then(response => {
        article.isRead = response.data.is_read; // 直接赋值更新阅读状态
    })
    .catch(error => {
        console.error('获取阅读状态出错：', error);
    });
};

//展示文章封面
const getArticles = () => {
    axios.get('http://localhost:5000/api/get_article')
    .then(response => {
        articles.data = response.data.map(article => ({
            ...article,
            isRead: false  // 初始化每篇文章的 isRead 属性
        })).reverse();
        // 检查每篇文章的阅读状态
        articles.data.forEach(article => {
            checkReadingStatus(article);
        });
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
    <div>
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
                <el-card class="article-card" @click="() => navigateToArticle(article.id)">
                    
                        <span class="title">{{ article.title }}</span>
                        <br />
                        <span class="time">{{ article.update_time }}</span>
                        <!-- {{ article.art_text.substring(0, 50) }}{{ article.art_text.length > 50 ? '...' : '' }} -->
                   
                    <div class="article-card-bottom">
                        <el-divider />
                        <div class="article-info">
                            <el-tag>{{ article.category }}</el-tag>
                            <el-icon v-if="article.isRead" style="color:#67c23a;"><CircleCheckFilled /></el-icon>
                        </div>
                    </div>
                </el-card>
            </div>
        </div>
        <h3>我的外刊</h3>
    </div>
</template>
    


<style scoped>


.time {
    position: absolute; /* 使用绝对定位 */
    top: 120px; /* 调整此值以使其位于分隔线上方的适当位置 */
    color: #909399;
}


.article-info {
  display: flex;
  justify-content: space-between; /* 类别和图标两端对齐 */
  align-items: center; /* 垂直居中 */
  padding: 10px; /* 适当内边距提升可读性 */
}
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
  position: relative; /* 设置为相对定位 */
  width: 100%; /* 确保卡片填满容器 */
  height: 150px; /* 高度自适应 */
  transition: background-color 0.3s; /* 平滑过渡效果 */
  background-color:white; /* 背景颜色 */
  padding-bottom: 60px; /* 为底部元素预留足够空间 */
 /* 确保内边距不影响宽高计算 */
}

.article-card-bottom {
  position: absolute; /* 绝对定位 */
  bottom: 0; /* 锚定至底部 */
  left: 0; /* 从左侧开始 */
  width: 100%; /* 与卡片同宽 */
}

.el-divider {
  margin-bottom: 8px; /* 分隔符下方留出空间 */
}

.article-card:hover {
  background-color:#ecf5ff; /* 鼠标悬浮时的背景颜色 */
}
</style>