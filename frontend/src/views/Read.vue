<script setup>
import Header from '../components/Header.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref, reactive, onMounted, watch,onBeforeUnmount} from 'vue';

import { ElMessage, ElButton, ElTable, ElTableColumn, ElInput } from 'element-plus';
import {Star, Delete, Edit, Check, UserFilled} from '@element-plus/icons-vue'

const route = useRoute();
const userId = ref('');
const article = reactive({
    data:{
        id: '',
        title: '',
        content: '',
    }
});
const isDisabled = ref();
let words_and_phrases = reactive({});
const table_data = ref([]);
const selectedText = ref('');
let role = ref('');
const inputMsg = ref('');
let grammar_analysis = ref('');

//测试聊天窗口
let msgList=reactive([
            {role: "system", msg: "How can I help you?",}, 
            // {role: "user", time: "", msg: "I'm Chloe",},
            // {role: "system", time: "", msg: "回答",},
        ])
let dialogue_history = ref('');
const dialogue_history_list = ref([]);
let dialogue_history_header = ref('');


// 组件挂载时获取文章数据
onMounted(() => {
    userId.value = sessionStorage.getItem('userId');
    document.addEventListener('mouseup', selectText);
    fetchArticle();
    show_words_and_phrases();
});

const addMsg = async (msg, role) => {
    inputMsg.value = '';
    const answer = ref('');
    msgList.push({
        role: role,
        msg: msg,
    });
    dialogue_history.value  = dialogue_history_header.value + msgList.slice(1).map(item => `${item.role}: ${item.msg}`).join('\n'); //问题应该在这，每次都会把msg.List中的元素加入到dialogue_history中，其实应该只要一遍

    
    if (role == 'user' ){
        try {
        const response = await axios.post('http://localhost:5000/api/chat', {
            msg: msg,
            dialogue_history: dialogue_history.value,
            sentence : selectedText.value
        });
        answer.value = response.data.answer;
        addMsg(answer.value, role='system');
        console.log("answer:",answer.value)
    } catch (error) {
        console.error('发送聊天内容到后端失败:', error);
    }
    }
    
}


const selectText = () => {
    if (window.getSelection) {
        selectedText.value = window.getSelection().toString().trim();
        console.log("selected text:",selectedText.value);
    }
};

const analyzeGrammar = async () => {
    if (selectedText.value) {
        ElMessage.success('语法分析中，请稍等...');
        try {
            const response = await axios.post('http://localhost:5000/api/analyze_grammar', {
                sentence: selectedText.value,
            });
            msgList.length = 1; //每一次对新的句子进行语法分析时自动清空对话历史
            
            if (response.data) {
                const prompt_header = response.data.prompt_header;
                // addMsg(prompt_header, role='user'); 
                dialogue_history_header.value = `user:${prompt_header}\n`; //聊天历史中的第一条记录是语法分析的prompt，但是不添加到msgList中,因为msgList中的记录会显示在聊天框中，而prompt_header不需要显示
                // console.log('第一条对话历史:', dialogue_history.value);
                prompt_analyze_grammar = response.data.prompt_header
                history_entry = {role: 'user', msg: prompt_analyze_grammar}
                
                dialogue_history_list.push(history_entry)

                role = 'system';
                const  msg = ref('');
                msg.value = response.data.grammar_analysis;
                grammar_analysis.value = msg.value;
                //addMsg(msg, role); //聊天历史中的第二条记录是语法分析的结果，也不需要显示在聊天框中
                dialogue_history_header.value += `system:${msg.value}\n`; 
                // console.log('第一和二条对话历史:', dialogue_history.value);
            }
        } catch (error) {
            console.error('语法分析出错:', error);
            ElMessage.error('语法分析失败，请检查服务器状态。');
        }
    } else {
        ElMessage.warning('请选择需要分析的文本！');
    }
};


const confirmRow = async (row) => {
  row.editable = false;
  try {
    const response = await axios.get('http://localhost:5000/api/add_term', {
        params:{
            article_id: route.params.id,
            user_id: userId.value,
            term: row.term,
            definition: row.definition
        }
    });
    ElMessage.success('添加成功');
  } catch (error) {
    console.error('添加词汇出错:', error);
    ElMessage.error('添加失败');
    // 如果失败，允许用户重新编辑
    row.editable = true;
  }
};

//新增可编辑行
const addRow = () => {
    const newRow = {
        term: '',
        definition: '',
        editable: true
    };
    table_data.value.push(newRow);
};

//删除某行
const deleteTerm = async (row) => {
    try {
        const response = await axios.get('http://localhost:5000/api/delete_term', {
            params:{id: row.id}
        });
        table_data.value = table_data.value.filter(term => term.id !== row.id);
    } catch (error) {
        console.error('删除词汇出错:', error);
    }
    };

const show_words_and_phrases = async() =>{
    try {
        const response = await axios.get(`http://localhost:5000/api/show_words_and_phrases`, {
            params: {
                article_id: route.params.id,  // 直接从 route.params 获取文章 ID
                user_id: userId.value
            }
        });
        isDisabled.value = response.data.is_disabled
        if(isDisabled.value){
            words_and_phrases = response.data.words_and_phrases
            table_data.value = words_and_phrases
        }
    } catch (error) {
        console.error('展示单词和短语时出错：', error);
    }

}

const extractWordsAndPhrases = async() => {
    ElMessage.success('抽取中，请稍等...');
    try {
        
        const response = await axios.get(`http://localhost:5000/api/extract_words_and_phrases`, {
            params: {
                article_id: route.params.id,  // 直接从 route.params 获取文章 ID
                user_id: userId.value
            }
        });
        console.log("单词和短语抽取状态：",response.data.message)
        show_words_and_phrases()

    } catch (error) {
        console.error('抽取单词和短语出错：', error);
    }
};

const props = defineProps({
    id: String
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

onBeforeUnmount(() => {
  document.removeEventListener('mouseup', selectText);
});
</script>

<template>
    <Header />
    <div class="container">
        <el-row>
            <el-col :span="14" class="art">
                <h1>{{ article.data.title }} </h1>
                <div>
                    <span style="margin-right: 10px;">{{ article.data.update_time }}</span> 
                    <span style="margin-right: 10px;">{{ article.data.article_source }}</span>
                    <el-button type="warning" :icon="Star" circle plain/>
                </div>
                <div v-html="article.data.content" @mouseup="selectText"></div>
            </el-col>
            <el-col :span="10" class="func">
                <h1>
                    <el-button type="primary" plain @click="extractWordsAndPhrases" :disabled="isDisabled">重点词汇短语</el-button>
                    <el-button type="warning" plain @click="analyzeGrammar">语法分析</el-button>
                </h1>
                <el-table :data="table_data" style="width: 100%">
                    <el-table-column prop="term" label="词汇或短语" width="200px">
                        <template #default="{row}">
                            <el-input v-model="row.term" v-if="row.editable"></el-input>
                            <div v-else>{{ row.term }}</div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="definition" label="解释" width="320px">
                        <template #default="{row}">
                            <el-input v-model="row.definition" v-if="row.editable"></el-input>
                            <div v-else>{{ row.definition }}</div>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作">
                        <template #default="{row}">
                            <el-button type="primary" plain icon = "Check" size='small' circle @click="() => confirmRow(row)" v-if="row.editable"></el-button>
                            <el-button type="danger"  plain icon="Delete" size='small' circle @click="deleteTerm(row)" v-else></el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-button @click="addRow" type="primary" plain style="margin-top: 10px; ">添加</el-button>
                <el-divider />
                <div v-html="grammar_analysis"></div>
                <!-- 添加聊天窗口 -->
                <div class="div1">
                    <div v-for="(msg,index) in msgList" :key="index">
                            <!-- 循环显示聊天记录 -->
                            <p :class="{'right':msg.role=='user'}">
                            <el-avatar v-if="msg.role=='system'" icon="UserFilled"></el-avatar>
                            <el-avatar v-if="msg.role=='user'" style="float:right;" src="../src/assets/user.jpg">user</el-avatar>
                            <span class="content">{{ msg.msg }}</span>
                            </p>
                    </div>
                    <div class="input-group">  <!-- 使用 flex 布局的 div -->
                        <el-input type="textarea" v-model="inputMsg" @keyup.enter="addMsg(inputMsg, role='user')" placeholder="请输入内容" clearable autosize></el-input>
                        <el-button  @click="addMsg(inputMsg, role='user')" icon="Position" type="warning" plain></el-button>
                    </div>
                    
                </div>
                <el-button type="warning" plain style="margin-top: 10px;">清空对话</el-button>

                



            </el-col>
        </el-row>
    </div>

</template>

<style scoped>
/* 聊天框输入框和按钮 */
.input-group {
  display: flex;  /* 启用 flex 布局 */
  align-items: center;  /* 垂直居中对齐 */
}

.input-group .el-input, 
.input-group .el-button {
  flex: 6, 1;  /* 输入框和按钮均可伸缩，但输入框可以占据更多空间 */
}

.input-group .el-button {
  margin-left: 10px;  /* 在按钮和输入框之间添加一些间隙 */
}



/* 聊天框窗口样式 */
.div1 {
    display: flex;
    flex-direction: column;
    padding: 10px;
    background: #f9f9f9;
    border: 1px solid #ccc;
    max-width: 600px;  /* 根据你的具体需要调整 */
    margin: auto;  /* 居中显示 */
}

.div1 > div {
    margin-bottom: 8px;
}

p {
    display: flex;
    align-items: flex-start;
    margin: 0;
}

.right {
    justify-content: flex-start;
    flex-direction: row-reverse; /* 添加这个属性来反转顺序 */
}

.el-avatar {
    margin-right: 10px;
    margin-left: 10px;
    min-width: 30px; /* 确保头像大小统一 */
}

.el-avatar[style*="float:right"] {
    margin-right: 0;
    margin-left: 10px;
}

span.content {
    background: antiquewhite;;
    border-radius: 15px;
    padding: 8px 12px;
    max-width: 80%;  /* 限制最大宽度，确保换行 */
    word-wrap: break-word;
}





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