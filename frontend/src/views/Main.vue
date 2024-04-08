<script setup>
import Header from '../components/Header.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';




</script>

<template>
    
    <Header/>
    <h3>外刊广场</h3>
    <div>
    <el-card v-for="article in articles" :key="article.id" class="article-card">
        <div slot="header" class="clearfix">
            <span>{{ article.title }}</span>
        </div>
        <div class="article-content">
            <p>{{ article.content }}</p>
            <p>类别: {{ article.category }}</p>
            <p>字数: {{ article.word_count }}</p>
        </div>
    </el-card>
    </div>
    
    
</template>

<style scoped>
.article-card {
    margin-bottom: 20px;
}

</style>