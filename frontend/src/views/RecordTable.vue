<template>
  <div class="page-card">
    <el-table :data="list" :empty-text="t('common.empty')" stripe>
      <el-table-column :label="t('borrow.borrower')" min-width="130"><template #default="{ row }">{{ row.user?.real_name }}</template></el-table-column>
      <el-table-column :label="t('borrow.book')" min-width="210"><template #default="{ row }">{{ bookTitle(row.book) }}</template></el-table-column>
      <el-table-column :label="t('borrow.borrowDate')" prop="borrow_date" />
      <el-table-column :label="t('borrow.dueDate')" prop="due_date" />
      <el-table-column :label="t('borrow.returnDate')"><template #default="{ row }">{{ row.return_date || '-' }}</template></el-table-column>
      <el-table-column :label="t('common.status')"><template #default="{ row }"><StatusTag :value="row.status" /></template></el-table-column>
      <el-table-column :label="t('common.actions')" width="130">
        <template #default="{ row }">
          <el-button v-if="row.status !== 'returned'" size="small" type="success" @click="$emit('return', row)">{{ t('borrow.returnBook') }}</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination">
      <el-pagination v-model:current-page="query.page" v-model:page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total" @change="$emit('page')" />
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import StatusTag from '../components/StatusTag.vue'
import { localBookTitle } from '../utils/format'

defineProps({ list: Array, total: Number, query: Object })
defineEmits(['page', 'return'])
const { t, locale } = useI18n()
const bookTitle = book => localBookTitle(book, locale.value)
</script>

