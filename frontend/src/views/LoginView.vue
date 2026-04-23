<template>
  <div class="login-page">
    <div class="login-card">
      <h1 class="login-title">{{ t('login.title') }}</h1>
      <p class="login-subtitle">{{ t('login.subtitle') }}</p>
      <el-form ref="formRef" :model="form" :rules="rules" size="large" @keyup.enter="submit">
        <el-form-item prop="username">
          <el-input v-model="form.username" :placeholder="t('login.username')" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" :placeholder="t('login.password')" prefix-icon="Lock" type="password" show-password />
        </el-form-item>
        <el-button type="primary" :loading="loading" style="width:100%" @click="submit">{{ t('login.button') }}</el-button>
      </el-form>
      <div style="margin-top:14px">
        <el-button text @click="setLang('zh-CN')">中文</el-button>
        <el-button text @click="setLang('en-US')">EN</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../store/auth'
import { useAppStore } from '../store/app'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()
const app = useAppStore()
const formRef = ref()
const loading = ref(false)
const form = reactive({ username: '', password: '' })
const rules = computed(() => ({
  username: [{ required: true, message: t('validate.required'), trigger: 'blur' }],
  password: [{ required: true, message: t('validate.required'), trigger: 'blur' }]
}))

function setLang(lang) {
  app.setLocale(lang)
}

async function submit() {
  await formRef.value.validate()
  loading.value = true
  try {
    await auth.login(form)
    ElMessage.success(t('common.success'))
    router.replace('/dashboard')
  } finally {
    loading.value = false
  }
}
</script>
