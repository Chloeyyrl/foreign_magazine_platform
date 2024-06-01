<script setup>
import { ref, reactive } from 'vue';
import { ElForm, ElFormItem, ElInput, ElButton, ElRow, ElCol, ElMessage, ElUpload } from 'element-plus';
import Header from '../components/Header.vue';
import axios from 'axios';

const uploadForm = reactive({
    title: '',
    category: '',
    source: ''
});
const rules = reactive({
    title: [
        { required: true, message: '请输入标题', trigger: 'blur' }
    ],
    category: [
        { required: true, message: '请输入类别', trigger: 'blur' }
    ],
    source: [
        { required: true, message: '请输入文章来源', trigger: 'blur' }
    ]
});
const formRef = ref(null);
const file = ref(null); // 文件引用
const userid = ref(sessionStorage.getItem('userId')); // 直接初始化

const resetForm = () => {
    formRef.value.resetFields();
    
};

const handleFileChange = (event) => {
    file.value = event.target.files[0]; // 更新文件引用
};

const onUpload = () => {
    formRef.value.validate(async (valid) => {
        if (valid && file.value) {
            const formData = new FormData();
            Object.keys(uploadForm).forEach(key => formData.append(key, uploadForm[key]));
            formData.append('file', file.value); // 添加文件到表单数据
            formData.append('userid', userid.value);

            try {
                const response = await axios.post('http://localhost:5000/api/upload', formData);
                if (response.status === 201) {
                    ElMessage.success(response.data.message);
                    resetForm(); // 成功后重置表单
                }
            } catch (error) {
                ElMessage.error('上传失败: ' + error.message);
            }
        } else {
            ElMessage.error('请填写完整信息并选择文件!');
        }
    });
};
</script>

<template>
    <Header />
    <el-row>
        <el-col :span="8"></el-col>
        <el-col :span="8">
            <h2>上传文章</h2>
            <el-form ref="formRef" :model="uploadForm" :rules="rules" label-width="100px" label-position="top">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="uploadForm.title" />
                </el-form-item>
                <el-form-item label="类别" prop="category">
                    <el-input v-model="uploadForm.category" />
                </el-form-item>
                <el-form-item label="来源" prop="source">
                    <el-input v-model="uploadForm.source" />
                </el-form-item>
                <el-form-item label="选择文件">
                    <input type="file" @change="handleFileChange" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onUpload">上传</el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>
            </el-form>
        </el-col>
        <el-col :span="8"></el-col>
    </el-row>
</template>


<style scoped>
/* 添加一些自定义样式 (如果需要) */
</style>
