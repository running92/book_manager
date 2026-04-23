<template>
  <div>
    <div class="toolbar">
      <div class="toolbar-left">
        <el-input v-model="query.keyword" clearable :placeholder="t('book.keyword')" style="width:240px" @keyup.enter="load" />
        <el-select v-model="query.status" clearable :placeholder="t('common.status')" style="width:150px">
          <el-option :label="t('common.borrowed')" value="borrowed" />
          <el-option :label="t('common.overdue')" value="overdue" />
          <el-option :label="t('common.returned')" value="returned" />
        </el-select>
        <el-button type="primary" icon="Search" @click="load">{{ t('common.search') }}</el-button>
        <el-button @click="reset">{{ t('common.reset') }}</el-button>
      </div>
      <el-button type="primary" icon="Plus" @click="openBorrow">{{ t('book.borrow') }}</el-button>
    </div>
    <RecordTable :list="list" :total="total" :query="query" @page="load" @return="returnRecord" />
    <el-dialog v-model="visible" :title="t('book.borrow')" width="520px">
      <el-form :model="borrowForm" label-width="110px">
        <el-form-item :label="t('borrow.borrower')">
          <el-select v-model="borrowForm.user_id" filterable style="width:100%">
            <el-option v-for="u in users" :key="u.id" :label="`${u.real_name} (${u.username})`" :value="u.id" />
          </el-select>
        </el-form-item>
        <el-form-item :label="t('borrow.book')">
          <el-select v-model="borrowForm.book_id" filterable style="width:100%">
            <el-option v-for="b in books" :key="b.id" :label="bookTitle(b)" :value="b.id" />
          </el-select>
        </el-form-item>
        <el-form-item :label="t('borrow.dueDate')"><el-input-number v-model="borrowForm.due_days" :min="1" :max="180" /></el-form-item>
        <el-form-item :label="t('borrow.remark')"><el-input v-model="borrowForm.remark" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">{{ t('common.cancel') }}</el-button>
        <el-button type="primary" @click="saveBorrow">{{ t('common.confirm') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { borrowBookApi, getBorrowRecordsApi, returnBookApi } from '../api/borrow'
import { getBooksApi } from '../api/books'
import { getUsersApi } from '../api/users'
import RecordTable from './RecordTable.vue'
import { localBookTitle } from '../utils/format'

const { t, locale } = useI18n()
const list = ref([])
const total = ref(0)
const visible = ref(false)
const users = ref([])
const books = ref([])
const query = reactive({ page: 1, page_size: 10, keyword: '', status: '' })
const borrowForm = reactive({ user_id: '', book_id: '', due_days: 30, remark: '' })
const bookTitle = book => localBookTitle(book, locale.value)

async function load() { const data = await getBorrowRecordsApi(query); list.value = data.items; total.value = data.total }
function reset() { Object.assign(query, { page: 1, page_size: 10, keyword: '', status: '' }); load() }
async function openBorrow() {
  visible.value = true
  users.value = (await getUsersApi({ page: 1, page_size: 100, role: 'reader', status: 'active' })).items
  books.value = (await getBooksApi({ page: 1, page_size: 100, status: 'available' })).items
}
async function saveBorrow() {
  await borrowBookApi(borrowForm)
  ElMessage.success(t('common.success'))
  visible.value = false
  load()
}
async function returnRecord(row) {
  await returnBookApi(row.id)
  ElMessage.success(t('common.success'))
  load()
}
onMounted(load)
</script>

