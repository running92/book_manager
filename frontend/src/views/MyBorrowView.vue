<template>
  <div>
    <div class="toolbar">
      <div class="toolbar-left">
        <el-select v-model="query.status" clearable :placeholder="t('common.status')" style="width:160px">
          <el-option :label="t('common.borrowed')" value="borrowed" />
          <el-option :label="t('common.overdue')" value="overdue" />
          <el-option :label="t('common.returned')" value="returned" />
        </el-select>
        <el-button type="primary" icon="Search" @click="load">{{ t('common.search') }}</el-button>
      </div>
    </div>
    <RecordTable :list="list" :total="total" :query="query" @page="load" @return="returnRecord" />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { getMyBorrowRecordsApi, returnBookApi } from '../api/borrow'
import RecordTable from './RecordTable.vue'

const { t } = useI18n()
const list = ref([])
const total = ref(0)
const query = reactive({ page: 1, page_size: 10, status: '' })
async function load() { const data = await getMyBorrowRecordsApi(query); list.value = data.items; total.value = data.total }
async function returnRecord(row) { await returnBookApi(row.id); ElMessage.success(t('common.success')); load() }
onMounted(load)
</script>

