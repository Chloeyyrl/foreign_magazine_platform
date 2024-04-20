<script setup>
import Header from '../components/Header.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref, reactive, onMounted} from 'vue';
import {Star} from '@element-plus/icons-vue'


const route = useRoute();
const userId = ref('');
const article = reactive({
    data:{
        id: '',
        title: '',
        content: '',
    }
});

const extractWordsAndPhrases = async() => {
    console.log("article_id:",route.params.id)
    console.log("user_id:",userId.value)
    try {
        const response = await axios.get(`http://localhost:5000/api/extract_words_and_phrases`, {
            params: {
                article_id: route.params.id,  // 直接从 route.params 获取文章 ID
                user_id: userId.value
            }
        });
    
        console.log("单词和短语抽取状态：",response.data.message)

    } catch (error) {
        console.error('抽取单词和短语出错：', error);
    }
};


const props = defineProps({
    id: String
});

// 组件挂载时获取文章数据
onMounted(() => {
    userId.value = sessionStorage.getItem('userId');
    fetchArticle();
});

const fetchArticle = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/api/get_article_info`, {
            params: {
                article_id: route.params.id,  // 直接从 route.params 获取文章 ID
                user_id: userId.value
            }
        });
        //console.log(route.params.id)
        article.data = response.data;  // 更新文章内容
    } catch (error) {
        console.error('获取文章信息出错：', error);
    }
};


</script>

<template>
    <Header />
    <div class="container">
        <el-row>
            <el-col :span="16" class="art">
                <h1>{{ article.data.title }} </h1>
                <div>
                    <span style="margin-right: 10px;">{{ article.data.update_time }}</span> 
                    <span style="margin-right: 10px;">{{ article.data.article_source }}</span>
                    <el-button type="warning" :icon="Star" circle plain/>
                </div>
                <div v-html="article.data.content"></div>
            </el-col>
            <el-col :span="8" class="func">
                <h1>
                    <el-button type="primary" plain @click="extractWordsAndPhrases">重点词汇短语</el-button>
                    <el-button type="success" plain>语法分析</el-button>
                    <el-button type="warning" plain>语境应用</el-button>
                </h1>
            </el-col>
        </el-row>
        
        
    </div>

</template>

<style scoped>
.align-span {
        display: flex;
        align-items: center; /* 确保所有项在交叉轴上居中对齐 */
    }
    .align-span span {
        margin-right: 10px; /* 给所有span标签右侧添加间隔 */
    }
    .align-span span:last-child {
        margin-right: 0; /* 最后一个span标签不需要右侧间隔 */
    }
.art{
    padding: 20px;
    border-right: 1px solid #ebeef5;
}
.func {
    padding: 20px;
}
</style>