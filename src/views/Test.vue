<script setup>

    </script>

    <template>
        <h3>图标</h3>
        <el-icon><Plus /></el-icon>
        <el-icon><Edit /></el-icon>
        <el-icon><Delete /></el-icon>
        <el-icon class="is-loading"><Loading /></el-icon>

        <hr>
        <h3>属性</h3>
        <el-icon size="30" color="red"><Search /></el-icon>

        <hr>
        <h3>按钮</h3>
        <el-button type="success">
            <el-icon><Search /></el-icon>
            <span> 搜索 </span>
        </el-button>

        <el-button type="primary">
            <el-icon><Search /></el-icon>
        </el-button>

        <el-button type="primary" circle>
            <el-icon><Search /></el-icon>
        </el-button>

        <hr>
        <h3>按钮组</h3>
        <el-button-group>
            <el-button type="primary">
                <el-icon><Plus /></el-icon>
            </el-button>

            <el-button type="primary">
                <el-icon><Edit /></el-icon>
            </el-button>

            <el-button type="primary">
                <el-icon><Delete /></el-icon>
            </el-button>
        </el-button-group>
    </template>

    <style scoped>

    </style>