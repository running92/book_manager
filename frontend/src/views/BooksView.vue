<template>
  <div>
    <div class="toolbar">
      <div class="toolbar-left">
        <el-input v-model="query.keyword" :placeholder="t('book.keyword')" clearable style="width:240px" @keyup.enter="load" />
        <el-select v-model="query.category_id" :placeholder="t('book.category')" clearable style="width:170px">
          <el-option v-for="c in categories" :key="c.id" :label="catName(c)" :value="c.id" />
        </el-select>
        <el-button type="primary" icon="Search" @click="load">{{ t('common.search') }}</el-button>
        <el-button @click="reset">{{ t('common.reset') }}</el-button>
      </div>
      <div class="toolbar-right">
        <el-button v-if="auth.isAdmin" type="primary" icon="Plus" @click="openForm()">{{ t('common.add') }}</el-button>
      </div>
    </div>
    <div class="page-card">
      <el-table :data="list" :empty-text="t('common.empty')" stripe>
        <el-table-column :label="t('book.cover')" width="80">
          <template #default="{ row }"><img v-if="row.cover_image" :src="assetUrl(row.cover_image)" class="book-cover" /><div v-else class="book-cover"></div></template>
        </el-table-column>
        <el-table-column :label="t('book.titleZh')" min-width="180"><template #default="{ row }">{{ bookTitle(row) }}</template></el-table-column>
        <el-table-column :label="t('book.isbn')" prop="isbn" width="150" />
        <el-table-column :label="t('book.author')" prop="author" />
        <el-table-column :label="t('book.category')"><template #default="{ row }">{{ catName(row.category) }}</template></el-table-column>
        <el-table-column :label="t('book.availableStock')" width="110"><template #default="{ row }">{{ row.available_stock }} / {{ row.total_stock }}</template></el-table-column>
        <el-table-column :label="t('common.status')" width="110"><template #default="{ row }"><StatusTag :value="row.status" /></template></el-table-column>
        <el-table-column :label="t('common.actions')" fixed="right" width="260">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/books/${row.id}`)">{{ t('common.detail') }}</el-button>
            <el-button v-if="auth.isAdmin" size="small" type="primary" @click="openForm(row)">{{ t('common.edit') }}</el-button>
            <el-button v-if="auth.isAdmin" size="small" type="danger" @click="remove(row)">{{ t('common.delete') }}</el-button>
            <el-button v-else size="small" type="success" :disabled="row.available_stock <= 0" @click="borrow(row)">{{ t('book.borrow') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination v-model:current-page="query.page" v-model:page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total" @change="load" />
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? t('common.edit') : t('common.add')" width="760px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="128px">
        <el-row :gutter="14">
          <el-col :span="12"><el-form-item :label="t('book.isbn')" prop="isbn"><el-input v-model="form.isbn" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item :label="t('book.author')" prop="author"><el-input v-model="form.author" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item :label="t('book.titleZh')" prop="title_zh"><el-input v-model="form.title_zh" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item :label="t('book.titleEn')" prop="title_en"><el-input v-model="form.title_en" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item :label="t('book.publisher')"><el-input v-model="form.publisher" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item :label="t('book.publishDate')"><el-input v-model="form.publish_date" placeholder="2024-01" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item :label="t('book.category')"><el-select v-model="form.category_id" style="width:100%"><el-option v-for="c in categories" :key="c.id" :label="catName(c)" :value="c.id" /></el-select></el-form-item></el-col>
          <el-col :span="12"><el-form-item :label="t('common.status')"><el-select v-model="form.status" style="width:100%"><el-option :label="t('common.available')" value="available" /><el-option :label="t('common.disabled')" value="disabled" /></el-select></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="t('book.totalStock')"><el-input-number v-model="form.total_stock" :min="0" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="t('book.availableStock')"><el-input-number v-model="form.available_stock" :min="0" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item :label="t('book.location')"><el-input v-model="form.location" /></el-form-item></el-col>
          <el-col :span="24">
            <el-form-item :label="t('book.cover')">
              <el-upload :show-file-list="false" :http-request="handleUpload"><el-button icon="Upload">{{ t('common.upload') }}</el-button></el-upload>
              <img v-if="form.cover_image" :src="assetUrl(form.cover_image)" class="book-cover" style="margin-left:12px" />
            </el-form-item>
          </el-col>
          <el-col :span="12"><el-form-item :label="t('book.descZh')"><el-input v-model="form.description_zh" type="textarea" :rows="3" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item :label="t('book.descEn')"><el-input v-model="form.description_en" type="textarea" :rows="3" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">{{ t('common.cancel') }}</el-button>
        <el-button type="primary" @click="save">{{ t('common.save') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage, ElMessageBox } from 'element-plus'
import { borrowBookApi } from '../api/borrow'
import { createBookApi, deleteBookApi, getBooksApi, updateBookApi, uploadCoverApi } from '../api/books'
import { getCategoriesApi } from '../api/categories'
import StatusTag from '../components/StatusTag.vue'
import { useAuthStore } from '../store/auth'
import { localBookTitle, localCategoryName } from '../utils/format'
import { assetUrl } from '../utils/url'

const { t, locale } = useI18n()
const auth = useAuthStore()
const list = ref([])
const total = ref(0)
const categories = ref([])
const dialogVisible = ref(false)
const formRef = ref()
const query = reactive({ page: 1, page_size: 10, keyword: '', category_id: '' })
const emptyForm = () => ({ id: null, isbn: '', title_zh: '', title_en: '', author: '', publisher: '', publish_date: '', category_id: '', cover_image: '', description_zh: '', description_en: '', total_stock: 1, available_stock: 1, location: '', status: 'available' })
const form = reactive(emptyForm())
const rules = computed(() => ({
  isbn: [{ required: true, message: t('validate.required'), trigger: 'blur' }],
  title_zh: [{ required: true, message: t('validate.required'), trigger: 'blur' }],
  title_en: [{ required: true, message: t('validate.required'), trigger: 'blur' }],
  author: [{ required: true, message: t('validate.required'), trigger: 'blur' }]
}))
const catName = cat => localCategoryName(cat, locale.value)
const bookTitle = book => localBookTitle(book, locale.value)

async function load() {
  const data = await getBooksApi(query)
  list.value = data.items
  total.value = data.total
}
async function loadCategories() { categories.value = await getCategoriesApi() }
function reset() { Object.assign(query, { page: 1, page_size: 10, keyword: '', category_id: '' }); load() }
function openForm(row) { Object.assign(form, emptyForm(), row || {}); dialogVisible.value = true }
async function handleUpload({ file }) { const data = await uploadCoverApi(file); form.cover_image = data.url }
async function save() {
  await formRef.value.validate()
  if (form.id) await updateBookApi(form.id, form)
  else await createBookApi(form)
  ElMessage.success(t('common.success'))
  dialogVisible.value = false
  load()
}
async function remove(row) {
  await ElMessageBox.confirm(t('common.deleteConfirm'), t('common.confirm'), { type: 'warning' })
  await deleteBookApi(row.id)
  ElMessage.success(t('common.success'))
  load()
}
async function borrow(row) {
  await borrowBookApi({ book_id: row.id })
  ElMessage.success(t('common.success'))
  load()
}
onMounted(() => { loadCategories(); load() })
</script>
