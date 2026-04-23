<template>
  <div class="grid-2">
    <div class="page-card">
      <h3>{{ t('profile.basic') }}</h3>
      <el-form :model="profile" label-width="110px">
        <el-form-item :label="t('user.username')"><el-input v-model="profile.username" disabled /></el-form-item>
        <el-form-item :label="t('user.realName')"><el-input v-model="profile.real_name" /></el-form-item>
        <el-form-item :label="t('user.phone')"><el-input v-model="profile.phone" /></el-form-item>
        <el-form-item :label="t('user.email')"><el-input v-model="profile.email" /></el-form-item>
        <el-button type="primary" @click="saveProfile">{{ t('common.save') }}</el-button>
      </el-form>
    </div>
    <div class="page-card">
      <h3>{{ t('profile.password') }}</h3>
      <el-form ref="pwdRef" :model="pwd" :rules="rules" label-width="120px">
        <el-form-item :label="t('profile.oldPassword')" prop="old_password"><el-input v-model="pwd.old_password" type="password" show-password /></el-form-item>
        <el-form-item :label="t('profile.newPassword')" prop="new_password"><el-input v-model="pwd.new_password" type="password" show-password /></el-form-item>
        <el-button type="primary" @click="savePassword">{{ t('common.save') }}</el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { changePasswordApi, updateProfileApi } from '../api/auth'
import { useAuthStore } from '../store/auth'

const { t } = useI18n()
const auth = useAuthStore()
const pwdRef = ref()
const profile = reactive({ username: '', real_name: '', phone: '', email: '' })
const pwd = reactive({ old_password: '', new_password: '' })
const rules = computed(() => ({
  old_password: [{ required: true, message: t('validate.required'), trigger: 'blur' }],
  new_password: [{ min: 6, message: t('validate.passwordLength'), trigger: 'blur' }]
}))
onMounted(() => Object.assign(profile, auth.user || {}))
async function saveProfile() {
  const data = await updateProfileApi(profile)
  auth.user = data
  localStorage.setItem('user', JSON.stringify(data))
  ElMessage.success(t('common.success'))
}
async function savePassword() {
  await pwdRef.value.validate()
  await changePasswordApi(pwd)
  Object.assign(pwd, { old_password: '', new_password: '' })
  ElMessage.success(t('common.success'))
}
</script>

