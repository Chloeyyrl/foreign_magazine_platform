<script setup>
import Header from '../components/Header.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref, reactive, onMounted} from 'vue';

const route = useRoute();
const articleId = route.params.id; 
const article = reactive({});
const userId = ref('');

// 组件挂载时获取文章数据
onMounted(() => {
    userId.value = sessionStorage.getItem('userId');
    getArticleInfo();
});

const getArticleInfo = async () => {
    try {
        const response = await axios.get('http://localhost:5000/api/get_article_info', {
            params: {
                articleId: articleId,
            }
        });

        
    } catch (error) {
        console.error('获取文章内容出错：', error);
    }
};

</script>

<template>
    <Header />
    <div class="container">
        <h1></h1>
    </div>

</template>

<style scoped>

</style>