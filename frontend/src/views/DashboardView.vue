<template>
  <div>
    <template v-if="auth.isAdmin">
      <div class="stat-grid">
        <div v-for="card in statCards" :key="card.label" class="stat-card" :style="{ background: card.color }">
          <div class="label">{{ card.label }}</div>
          <div class="value">{{ card.value }}</div>
        </div>
      </div>
      <div class="grid-2">
        <div class="page-card">
          <h3>{{ t('dashboard.trend') }}</h3>
          <div ref="trendRef" class="chart-box"></div>
        </div>
        <div class="page-card">
          <h3>{{ t('dashboard.category') }}</h3>
          <div ref="categoryRef" class="chart-box"></div>
        </div>
      </div>
      <div class="page-card" style="margin-top:18px">
        <h3>{{ t('dashboard.recent') }}</h3>
        <el-table :data="stats.recent_records || []" empty-text="No Data">
          <el-table-column :label="t('borrow.borrower')" prop="user.real_name" />
          <el-table-column :label="t('borrow.book')">
            <template #default="{ row }">{{ bookTitle(row.book) }}</template>
          </el-table-column>
          <el-table-column :label="t('borrow.borrowDate')" prop="borrow_date" />
          <el-table-column :label="t('common.status')"><template #default="{ row }"><StatusTag :value="row.status" /></template></el-table-column>
        </el-table>
      </div>
    </template>

    <template v-else>
      <div class="grid-2">
        <div class="page-card">
          <h3>{{ t('dashboard.myCurrent') }}</h3>
          <el-table :data="stats.my_current || []" :empty-text="t('common.empty')">
            <el-table-column :label="t('borrow.book')"><template #default="{ row }">{{ bookTitle(row.book) }}</template></el-table-column>
            <el-table-column :label="t('borrow.dueDate')" prop="due_date" />
            <el-table-column :label="t('common.status')"><template #default="{ row }"><StatusTag :value="row.status" /></template></el-table-column>
          </el-table>
        </div>
        <div class="page-card">
          <h3>{{ t('dashboard.reminders') }}</h3>
          <el-empty v-if="!stats.reminders?.length" :description="t('common.empty')" />
          <el-alert v-for="item in stats.reminders" :key="item.id" :title="`${bookTitle(item.book)} - ${item.due_date}`" :type="item.status === 'overdue' ? 'error' : 'warning'" show-icon style="margin-bottom:10px" />
        </div>
      </div>
      <div class="page-card" style="margin-top:18px">
        <h3>{{ t('dashboard.recommended') }}</h3>
        <div class="book-card-list">
          <div v-for="book in stats.recommended_books || []" :key="book.id" class="book-mini">
            <strong>{{ bookTitle(book) }}</strong>
            <p class="muted">{{ book.author }}</p>
            <el-button type="primary" size="small" @click="$router.push(`/books/${book.id}`)">{{ t('common.detail') }}</el-button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { LineChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { computed, nextTick, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { getDashboardStatsApi } from '../api/dashboard'
import StatusTag from '../components/StatusTag.vue'
import { useAuthStore } from '../store/auth'
import { localBookTitle } from '../utils/format'

echarts.use([LineChart, PieChart, GridComponent, TooltipComponent, CanvasRenderer])

const { t, locale } = useI18n()
const auth = useAuthStore()
const stats = ref({})
const trendRef = ref()
const categoryRef = ref()
const bookTitle = book => localBookTitle(book, locale.value)

const statCards = computed(() => [
  { label: t('dashboard.bookTotal'), value: stats.value.book_total || 0, color: '#2563eb' },
  { label: t('dashboard.availableTotal'), value: stats.value.available_total || 0, color: '#059669' },
  { label: t('dashboard.borrowedTotal'), value: stats.value.borrowed_total || 0, color: '#f59e0b' },
  { label: t('dashboard.userTotal'), value: stats.value.user_total || 0, color: '#7c3aed' },
  { label: t('dashboard.currentBorrow'), value: stats.value.current_borrow_total || 0, color: '#0891b2' },
  { label: t('dashboard.recordTotal'), value: stats.value.record_total || 0, color: '#db2777' }
])

async function load() {
  stats.value = await getDashboardStatsApi()
  await nextTick()
  if (auth.isAdmin) renderCharts()
}

function renderCharts() {
  echarts.init(trendRef.value).setOption({
    tooltip: {},
    xAxis: { type: 'category', data: (stats.value.borrow_trend || []).map(x => x.date.slice(5)) },
    yAxis: { type: 'value' },
    series: [{ type: 'line', smooth: true, areaStyle: {}, data: (stats.value.borrow_trend || []).map(x => x.count) }]
  })
  echarts.init(categoryRef.value).setOption({
    tooltip: { trigger: 'item' },
    series: [{ type: 'pie', radius: ['40%', '70%'], data: (stats.value.category_distribution || []).map(x => ({ name: locale.value === 'en-US' ? x.name_en : x.name_zh, value: x.value })) }]
  })
}

onMounted(load)
</script>
