<template>
  <div class="page-card">
    <el-button icon="ArrowLeft" @click="$router.back()">{{ t('common.back') }}</el-button>
    <el-row :gutter="24" style="margin-top:18px">
      <el-col :span="6">
        <img v-if="book.cover_image" :src="book.cover_image" style="width:100%;border-radius:8px" />
        <div v-else style="height:280px;background:#e5e7eb;border-radius:8px"></div>
      </el-col>
      <el-col :span="18">
        <h2 class="detail-title">{{ bookTitle(book) }}</h2>
        <p class="muted">{{ book.author }} · {{ book.publisher }}</p>
        <el-descriptions :column="2" border>
          <el-descriptions-item :label="t('book.isbn')">{{ book.isbn }}</el-descriptions-item>
          <el-descriptions-item :label="t('book.category')">{{ catName(book.category) }}</el-descriptions-item>
          <el-descriptions-item :label="t('book.availableStock')">{{ book.available_stock }} / {{ book.total_stock }}</el-descriptions-item>
          <el-descriptions-item :label="t('book.location')">{{ book.location }}</el-descriptions-item>
          <el-descriptions-item :label="t('common.status')"><StatusTag :value="book.status" /></el-descriptions-item>
        </el-descriptions>
        <p style="line-height:1.8">{{ locale === 'en-US' ? book.description_en : book.description_zh }}</p>
        <el-button v-if="!auth.isAdmin" type="success" :disabled="book.available_stock <= 0" @click="borrow">{{ t('book.borrow') }}</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { borrowBookApi } from '../api/borrow'
import { getBookApi } from '../api/books'
import StatusTag from '../components/StatusTag.vue'
import { useAuthStore } from '../store/auth'
import { localBookTitle, localCategoryName } from '../utils/format'

const { t, locale } = useI18n()
const route = useRoute()
const auth = useAuthStore()
const book = ref({})
const bookTitle = b => localBookTitle(b, locale.value)
const catName = c => localCategoryName(c, locale.value)
async function load() { book.value = await getBookApi(route.params.id) }
async function borrow() { await borrowBookApi({ book_id: book.value.id }); ElMessage.success(t('common.success')); load() }
onMounted(load)
</script>

