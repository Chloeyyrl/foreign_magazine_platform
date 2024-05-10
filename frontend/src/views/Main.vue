<script setup>
import Header from '../components/Header.vue';
import { ref, reactive, onMounted} from 'vue';
import { useRouter } from 'vue-router';
import { Search } from '@element-plus/icons-vue'

import axios from 'axios';

const articles = reactive({ data: [] });
const showAll = ref(false);
const articles_user_uploaded = reactive({ data: [] });
const showAll_user_uploaded = ref(false);
const userId = ref('');
const router = useRouter(); // 使用路由
const searchContent = ref(''); 

// 组件挂载时获取文章数据
onMounted(() => {
    userId.value = sessionStorage.getItem('userId');
    getArticles();
    getArticles_user_uploaded();
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

// 跳转到上传文章页
const goToUpload = () => {
    router.push('/upload').catch(error => {
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

//展示文章封面（用户上传部分）
const getArticles_user_uploaded = () => {
    axios.get('http://localhost:5000/api/get_article_user_uploaded', {
        params: {
            userId: userId.value,
        }
    })
    .then(response => {
        articles_user_uploaded.data = response.data.map(article => ({
            ...article,
            isRead: false  // 初始化每篇文章的 isRead 属性
        })).reverse();
        console.log(articles_user_uploaded.data);
        // 检查每篇文章的阅读状态
        articles_user_uploaded.data.forEach(article => {
            checkReadingStatus(article);
        });
    })
    .catch(error => {
        console.error('获取文章内容出错：', error);
    });
}


const displayedArticles = () => {
    return showAll.value ? articles.data : articles.data.slice(0,4);
};

const displayedArticles_user_uploaded = () => {
    return showAll_user_uploaded.value ? articles_user_uploaded.data : articles_user_uploaded.data.slice(0,4);
};

// 切换展示状态的方法
const toggleShowAll = () => {
    showAll.value = !showAll.value;
};

const toggleShowAll_user_uploaded = () => {
    showAll_user_uploaded.value = !showAll_user_uploaded.value;
};

const SearchKeywords = (searchContent) => {
    axios.get('http://localhost:5000/api/search_article', {
        params: {
            searchContent: searchContent,
            user_id : userId.value
        }
    })
    .then(response => {
        articles.data = response.data.filtered_articles.map(article => ({
            ...article,
            isRead: false  // 初始化每篇文章的 isRead 属性
        })).reverse();
        // 检查每篇文章的阅读状态
        articles.data.forEach(article => {
            checkReadingStatus(article);
        });

        articles_user_uploaded.data = response.data.filterd_articles_user.map(article => ({
            ...article,
            isRead: false  // 初始化每篇文章的 isRead 属性
        })).reverse();
        console.log("!!1!11!",articles_user_uploaded.data);
        // 检查每篇文章的阅读状态
        articles_user_uploaded.data.forEach(article => {
            checkReadingStatus(article);
        });

    })
    .catch(error => {
        console.error('获取限定文章内容出错：', error);
    });
};
</script>

<template>
    <div>
        <Header/>
        <el-row>
            <el-col :span="8"></el-col>
            <el-col :span="8" style="margin-top: 30px; margin-left: 20px;"> 
                <el-input
                    v-model="searchContent"
                    placeholder="请输入搜索内容"
                    :suffix-icon="Search"
                    @keyup.enter="SearchKeywords(searchContent)"
                    />
            </el-col>
        </el-row>
        <div class="header-container">
            <h3>文章中心</h3>
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
                    <div class="article-card-bottom">
                        <el-divider />
                        <div class="article-info">
                            <el-tag>{{ article.category }}</el-tag>
                            <el-icon v-if="article.isRead" style="color:#67c23a;" size="large"><CircleCheckFilled /></el-icon>
                        </div>
                    </div>
                </el-card>
            </div>
        </div>

        <div class="header-container">
            <h3>我的文章 <el-button type="primary" plain @click="goToUpload()">上传文件</el-button></h3>
            <el-button v-if="articles_user_uploaded.data.length > 4" @click="toggleShowAll_user_uploaded" type="primary" plain>
                {{ showAll_user_uploaded ? '点击收起' : '展开全部' }}
                <el-icon class="icon-space"><ArrowDown /></el-icon>
            </el-button>
        </div>

        <div class="articles-row">
            <div v-for="article in displayedArticles_user_uploaded()" :key="article.id" class="article-card-container">
                <el-card class="article-card" @click="() => navigateToArticle(article.id)">
                    
                        <span class="title">{{ article.title }}</span>
                        <br />
                        <span class="time">{{ article.update_time }}</span>
                    <div class="article-card-bottom">
                        <el-divider />
                        <div class="article-info">
                            <el-tag>{{ article.category }}</el-tag>
                            <el-icon v-if="article.isRead" style="color:#67c23a;" size="large"><CircleCheckFilled /></el-icon>
                        </div>
                    </div>
                </el-card>
                
            </div>
            
        </div>
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
    margin-left: 20px;
    margin-right: 20px;
    margin-top: 10px;
    margin-bottom: 10px;
}

.articles-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start; /* Or 'space-between' if you want equal spacing */
  margin: -8px; /* Adjust this value based on your gap preference */
  margin-left: 10px;
  margin-right: 10px;
}

.article-card-container {
  flex: 0 0 25%; /* This ensures that each card takes up 25% of the container's width */
  max-width: 25%; /* This ensures that each card's maximum width is 25% of the container's width */
  padding: 10px; /* Adjust this value based on your gap preference */
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