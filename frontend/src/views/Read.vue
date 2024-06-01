<script setup>
import Header from '../components/Header.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref, reactive, onMounted, computed, watch} from 'vue';

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

let words_and_phrases = reactive({});
const table_data = ref([]);
const selectedText = ref('');
const inputMsg = ref('');
let grammar_analysis = ref(''); //接收语法分析结果，展示在前端页面
let highlightTerms = ref([]); //接收高亮的单词或短语


//聊天窗口
let msgList=reactive(
        [
            {role: "assistant", msg: "有什么我可以帮忙的吗？"}, 
        ])
let dialogue_history = ref('');
const dialogue_history_list = reactive([]);

// 定义音频地址列表和当前索引
const audioState = reactive({
  files: [],
  currentIndex: null
});
const audioPlayer = ref(null);

// 组件挂载时获取文章数据
onMounted(() => {
    userId.value = sessionStorage.getItem('userId');
    document.addEventListener('mouseup', selectText);
    fetchArticle();
    show_words_and_phrases();
    
    audioPlayer.value.addEventListener('ended', nextAudio);

   
});



// 语音播放
//  根据句子结束符分割文本
// let currentIndex = 0;
// const speak = () => {
    
//     const textParts = article.data.art_text.split(/[\.\?!;]\s/); 
//     if (currentIndex >= textParts.length) {
//         console.log("朗读完毕");
//         return;  // 所有部分已朗读完毕
//     }
//     if (speechSynthesis.speaking) {
//         speechSynthesis.cancel(); // 停止当前的朗读以防重叠
//     }
//     const utterance = new SpeechSynthesisUtterance(textParts[currentIndex]);
//     utterance.lang = 'en-US';  // 确保语言设置匹配文本语言
//     utterance.onend = () => {
//         console.log("完成朗读段落：", textParts[currentIndex]);
//         currentIndex++;  // 移动到下一个部分
//         speak();  // 朗读下一部分
//     };
//     utterance.onerror = (event) => {
//         console.error('朗读发生错误:', event.error);
//     };

//     speechSynthesis.speak(utterance);
//     console.log("正在朗读：", textParts[currentIndex]);
// }


// const  pause = () => {
//   if (speechSynthesis.speaking) {
//     speechSynthesis.pause();
//   }
// }

// const resume = () => {
//   if (speechSynthesis.paused) {
//     speechSynthesis.resume();
//   }
// }

const finishReading = () => {
    try {
        axios.post('http://localhost:5000/api/finish_reading', 
            {
                article_id: route.params.id,
                user_id: userId.value
            }
        );
        ElMessage.success('祝贺！');
    } catch (error) {
        console.error('阅读状态修改出错:', error);
        ElMessage.error('完成阅读失败');
    }
    
}

const clearMsg = () => {
    msgList.length = 1;
}


const addMsg = async (role, msg) => {
    const answer = ref('');

    //Clear the input box
    inputMsg.value = ''; 

    //Append role and msg to the msgList and dialogue_history_list
    msgList.push({ role: role, msg: msg });
    dialogue_history_list.push({role: role, content: msg})
    
    //Format the chat history
    dialogue_history.value = dialogue_history_list.map(entry => `${entry.role}:${entry.content}`).join('\n')

    if (role == 'user' ){
        try {
        const response = await axios.post('http://localhost:5000/api/chat', {
            dialogue_history: dialogue_history.value,
        });
        answer.value = response.data.answer;
        addMsg(role='assistant',msg=answer.value);
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
                const analyze_grammar_prompt = ref('')
                let dialogue_history_entry = ref({})

                analyze_grammar_prompt.value = selectedText.value
                dialogue_history_entry = {role: 'user', content: analyze_grammar_prompt.value}
                dialogue_history_list.push(dialogue_history_entry)

                // analyze_grammar_prompt.value = response.data.analyze_grammar_prompt
                // dialogue_history_entry = {role: 'user', content: analyze_grammar_prompt.value}
                // dialogue_history_list.push(dialogue_history_entry) //第一条对话历史记录，要存入对话历史记录

                grammar_analysis.value = response.data.grammar_analysis;
                // dialogue_history_entry = {role: 'assistant', content: grammar_analysis.value}
                // dialogue_history_list.push(dialogue_history_entry) //第二条对话历史记录，要存入对话历史记录
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
    fetchArticle();
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
        fetchArticle();
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
        
        
            words_and_phrases = response.data.words_and_phrases
            table_data.value = words_and_phrases
        
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
        show_words_and_phrases();
        fetchArticle();

    } catch (error) {
        console.error('抽取单词和短语出错：', error);
        ElMessage.error('抽取失败，请检查服务器状态。');
    }
};

const props = defineProps({
    id: String
});

// 观察词汇列表和文章内容变化并更新高亮内容
// watchEffect(() => {
//   highlightedContent.value = article.data.content; // 先设置为原始文章内容
//   highlightTerms.value.forEach(term => {
//     const regex = new RegExp(`(${term.term})`, 'gi');
//     highlightedContent.value = highlightedContent.value.replace(regex, `<mark style='background-color:#d1edc4'>$1</mark>`);
//   });
// });


console.log(audioState.currentIndex)

const fetchArticle = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/api/get_article_info`, {
            params: {
                article_id: route.params.id,  // 直接从 route.params 获取文章 ID
                user_id: userId.value
            }
        });
        
        article.data = response.data.article;  // 更新文章内容
        highlightTerms = response.data.highlighted_terms

        console.log('高亮短语：-----',highlightTerms)
        
        highlightTerms.forEach(term => {   
        const regex = new RegExp(`(${term['term']})`);
        article.data.content = article.data.content.replace(regex, `<mark style='background-color:#d1edc4'>$1</mark>`);
    });

        audioState.currentIndex = 0; // 设置音频索引
        const audioList = article.data.audio_path.split(',')
        console.log('audioList:',audioList)
        for (let i = 0; i < audioList.length-1; i++) {
            audioState.files.push(audioList[i])
            
        }
        

    } catch (error) {
        console.error('获取文章信息出错：', error);
    }
};

//组件挂载后，获取音频文件地址
// fetchAudioFiles = async () => {
//   try {
//     const response = await axios.get('http://localhost:5000/api/get_audio_files');
//     audioState.files = response.data.files;
//   } catch (error) {
//     console.error('获取音频文件地址出错:', error);
//   }
// };







const prevAudio = () => {
  if (audioState.currentIndex > 0) {
    audioState.currentIndex -= 1;
  } else {
    audioState.currentIndex = audioState.files.length - 1; // 循环到最后一个
  }
};

const nextAudio = () => {
  if (audioState.currentIndex < audioState.files.length - 1) {
    audioState.currentIndex += 1; // 更新索引
  } else {
    audioState.currentIndex = 0; // 循环到第一个
  }
};

watch(() => audioState.currentIndex, (newIndex,oldIndex) => {
    if(oldIndex == null | newIndex == oldIndex | newIndex == 0 && oldIndex != 0 ){
        audioPlayer.value.load(); 
    }
    else{
        audioPlayer.value.load(); 
        audioPlayer.value.play(); 
        
    }
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

                </div>

                <div class="audio-player">
                    <audio ref="audioPlayer" controls class="audio-control">
                        <source :src="audioState.files[audioState.currentIndex]" type="audio/mpeg" />
                    </audio>
                    
                    <div class="button-group">
                        <el-button type="success" plain  @click="prevAudio"><el-icon><CaretLeft /></el-icon></el-button>
                        <el-button type="success" plain  @click="nextAudio"><el-icon><CaretRight /></el-icon></el-button>
                    </div>
                </div>


                <div v-html="article.data.content" @mouseup="selectText"></div>
                <div style="padding-top: 5px;"><el-button type="primary" plain @click="finishReading">完成阅读</el-button></div>
                <el-backtop :bottom="30">
                    <div
                    style="
                        height: 100%;
                        width: 100%;
                        background-color: var(--el-bg-color-overlay);
                        box-shadow: var(--el-box-shadow-lighter);
                        text-align: center;
                        line-height: 40px;
                        color: #409eff;
                    "
                    >
                    <el-icon><Top /></el-icon>
                    </div>
                </el-backtop>
            </el-col>
            <el-col :span="10" class="func">
                <h1>
                    <el-button type="primary" plain @click="extractWordsAndPhrases" >重点词汇短语</el-button>
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
                    <el-table-column label="操作" >
                        <template #default="{row}">
                            <el-button type="primary" plain icon = "Check" size='small'  @click="() => confirmRow(row)" v-if="row.editable"></el-button>
                            <el-button type="danger"  plain icon="Delete" size='small'  @click="deleteTerm(row)" v-else></el-button>
        
                        </template>
                    </el-table-column>
                </el-table>
                <el-button @click="addRow" type="primary" plain style="margin-top: 10px; ">添加</el-button>
                <el-divider />
                <div v-html="grammar_analysis" style="margin-bottom: 10px;"></div>
                <!-- 添加聊天窗口 -->
                <div class="div1">
                    <div v-for="(msg,index) in msgList" :key="index">
                            <!-- 循环显示聊天记录 -->
                            <p :class="{'right':msg.role=='user'}">
                            <el-avatar v-if="msg.role=='assistant'" icon="UserFilled"></el-avatar>
                            <el-avatar v-if="msg.role=='user'" style="float:right;" src="../src/assets/user.jpg">user</el-avatar>
                            <span class="content">{{ msg.msg }}</span>
                            </p>
                    </div>
                    <div class="input-group">  <!-- 使用 flex 布局的 div -->
                        <el-input type="textarea" v-model="inputMsg" @keyup.enter="addMsg('user', inputMsg)" placeholder="请输入内容" clearable autosize></el-input>
                        <el-button  @click="addMsg('user', inputMsg)" icon="Position" type="warning" plain></el-button>
                    </div>
                    
                </div>
                <el-button type="warning" plain style="margin-top: 10px" @click="clearMsg"> 清空对话</el-button>

                



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


.audio-player {
  display: flex; /* 使用Flexbox进行布局 */
  align-items: center; /* 垂直居中对齐所有子元素 */
  justify-content: flex-start; /* 元素向左对齐 */
}

.audio-control {
    
  width: 450px; /* 同时设置一个最大宽度限制 */
  margin-right: 10px; /* 右边距，确保与按钮组有间隔 */
  margin-top: 10px;
  margin-bottom: 5px;
  height:40px;
  
}

.button-group {
  display: flex; /* 确保按钮在同一行 */
  align-items: center; /* 按钮垂直居中 */
}



</style>