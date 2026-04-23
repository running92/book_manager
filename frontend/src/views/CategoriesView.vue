<template>
  <div>
    <div class="toolbar">
      <div class="toolbar-left"></div>
      <el-button type="primary" icon="Plus" @click="openForm()">{{ t('common.add') }}</el-button>
    </div>
    <div class="page-card">
      <el-table :data="list" :empty-text="t('common.empty')">
        <el-table-column :label="t('category.nameZh')" prop="name_zh" />
        <el-table-column :label="t('category.nameEn')" prop="name_en" />
        <el-table-column :label="t('category.description')" prop="description" />
        <el-table-column :label="t('category.sortOrder')" prop="sort_order" width="100" />
        <el-table-column :label="t('common.actions')" width="180">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="openForm(row)">{{ t('common.edit') }}</el-button>
            <el-button size="small" type="danger" @click="remove(row)">{{ t('common.delete') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="visible" :title="form.id ? t('common.edit') : t('common.add')" width="520px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item :label="t('category.nameZh')" prop="name_zh"><el-input v-model="form.name_zh" /></el-form-item>
        <el-form-item :label="t('category.nameEn')" prop="name_en"><el-input v-model="form.name_en" /></el-form-item>
        <el-form-item :label="t('category.description')"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item :label="t('category.sortOrder')"><el-input-number v-model="form.sort_order" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">{{ t('common.cancel') }}</el-button>
        <el-button type="primary" @click="save">{{ t('common.save') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage, ElMessageBox } from 'element-plus'
import { createCategoryApi, deleteCategoryApi, getCategoriesApi, updateCategoryApi } from '../api/categories'

const { t } = useI18n()
const list = ref([])
const visible = ref(false)
const formRef = ref()
const base = () => ({ id: null, name_zh: '', name_en: '', description: '', sort_order: 0 })
const form = reactive(base())
const rules = computed(() => ({
  name_zh: [{ required: true, message: t('validate.required'), trigger: 'blur' }],
  name_en: [{ required: true, message: t('validate.required'), trigger: 'blur' }]
}))
async function load() { list.value = await getCategoriesApi() }
function openForm(row) { Object.assign(form, base(), row || {}); visible.value = true }
async function save() {
  await formRef.value.validate()
  if (form.id) await updateCategoryApi(form.id, form)
  else await createCategoryApi(form)
  ElMessage.success(t('common.success'))
  visible.value = false
  load()
}
async function remove(row) {
  await ElMessageBox.confirm(t('common.deleteConfirm'), t('common.confirm'), { type: 'warning' })
  await deleteCategoryApi(row.id)
  ElMessage.success(t('common.success'))
  load()
}
onMounted(load)
</script>

