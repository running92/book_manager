<template>
  <el-tag :type="typeMap[value] || 'info'" effect="light">{{ label }}</el-tag>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({ value: { type: String, default: '' } })
const { t } = useI18n()
const typeMap = {
  active: 'success',
  disabled: 'info',
  available: 'success',
  borrowed: 'warning',
  returned: 'success',
  overdue: 'danger'
}
const keyMap = {
  active: 'common.enabled',
  disabled: 'common.disabled',
  available: 'common.available',
  borrowed: 'common.borrowed',
  returned: 'common.returned',
  overdue: 'common.overdue'
}
const label = computed(() => t(keyMap[props.value] || 'common.unavailable'))
</script>

