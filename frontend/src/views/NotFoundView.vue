<template>
  <div class="login-page">
    <div class="login-card" style="text-align:center">
      <h1 class="login-title">404</h1>
      <p class="login-subtitle">{{ t('notFound.title') }}</p>
      <el-button type="primary" @click="$router.replace('/dashboard')">{{ t('notFound.backHome') }}</el-button>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

