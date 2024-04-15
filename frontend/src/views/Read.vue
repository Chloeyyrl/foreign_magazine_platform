<script setup>
import Header from '../components/Header.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref, reactive, onMounted} from 'vue';

const route = useRoute();
const article = reactive({
    data:{
        id: '',
        title: '',
        content: '',
        

    }
});
const userId = ref('');

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
        console.log(article.data.id)
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
                </div>
                <div v-html="article.data.content"></div>
            </el-col>
            <el-col :span="8">
                <h2>功能区</h2>
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
</style>