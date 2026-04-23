<template>
  <div>
    <div class="toolbar">
      <div class="toolbar-left">
        <el-input v-model="query.keyword" clearable :placeholder="t('user.username')" style="width:220px" @keyup.enter="load" />
        <el-select v-model="query.role" clearable :placeholder="t('user.role')" style="width:140px">
          <el-option :label="t('app.admin')" value="admin" /><el-option :label="t('app.reader')" value="reader" />
        </el-select>
        <el-button type="primary" icon="Search" @click="load">{{ t('common.search') }}</el-button>
        <el-button @click="reset">{{ t('common.reset') }}</el-button>
      </div>
      <el-button type="primary" icon="Plus" @click="openForm()">{{ t('common.add') }}</el-button>
    </div>
    <div class="page-card">
      <el-table :data="list" :empty-text="t('common.empty')">
        <el-table-column :label="t('user.username')" prop="username" />
        <el-table-column :label="t('user.realName')" prop="real_name" />
        <el-table-column :label="t('user.role')"><template #default="{ row }">{{ row.role === 'admin' ? t('app.admin') : t('app.reader') }}</template></el-table-column>
        <el-table-column :label="t('user.phone')" prop="phone" />
        <el-table-column :label="t('user.email')" prop="email" />
        <el-table-column :label="t('common.status')"><template #default="{ row }"><StatusTag :value="row.status" /></template></el-table-column>
        <el-table-column :label="t('common.actions')" width="300">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="openForm(row)">{{ t('common.edit') }}</el-button>
            <el-button size="small" @click="resetPassword(row)">{{ t('user.resetPassword') }}</el-button>
            <el-button size="small" type="danger" @click="remove(row)">{{ t('common.delete') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination"><el-pagination v-model:current-page="query.page" v-model:page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total" @change="load" /></div>
    </div>
    <el-dialog v-model="visible" :title="form.id ? t('common.edit') : t('common.add')" width="560px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="110px">
        <el-form-item :label="t('user.username')" prop="username"><el-input v-model="form.username" :disabled="Boolean(form.id)" /></el-form-item>
        <el-form-item v-if="!form.id" :label="t('user.password')" prop="password"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-form-item :label="t('user.realName')" prop="real_name"><el-input v-model="form.real_name" /></el-form-item>
        <el-form-item :label="t('user.role')"><el-select v-model="form.role" style="width:100%"><el-option :label="t('app.admin')" value="admin" /><el-option :label="t('app.reader')" value="reader" /></el-select></el-form-item>
        <el-form-item :label="t('common.status')"><el-select v-model="form.status" style="width:100%"><el-option :label="t('common.enabled')" value="active" /><el-option :label="t('common.disabled')" value="disabled" /></el-select></el-form-item>
        <el-form-item :label="t('user.phone')"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item :label="t('user.email')"><el-input v-model="form.email" /></el-form-item>
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
import { createUserApi, deleteUserApi, getUsersApi, resetPasswordApi, updateUserApi } from '../api/users'
import StatusTag from '../components/StatusTag.vue'

const { t } = useI18n()
const list = ref([])
const total = ref(0)
const visible = ref(false)
const formRef = ref()
const query = reactive({ page: 1, page_size: 10, keyword: '', role: '' })
const base = () => ({ id: null, username: '', password: '123456', real_name: '', role: 'reader', phone: '', email: '', status: 'active' })
const form = reactive(base())
const rules = computed(() => ({
  username: [{ required: true, message: t('validate.required'), trigger: 'blur' }],
  password: [{ min: 6, message: t('validate.passwordLength'), trigger: 'blur' }],
  real_name: [{ required: true, message: t('validate.required'), trigger: 'blur' }]
}))
async function load() { const data = await getUsersApi(query); list.value = data.items; total.value = data.total }
function reset() { Object.assign(query, { page: 1, page_size: 10, keyword: '', role: '' }); load() }
function openForm(row) { Object.assign(form, base(), row || {}); visible.value = true }
async function save() {
  await formRef.value.validate()
  if (form.id) await updateUserApi(form.id, form)
  else await createUserApi(form)
  ElMessage.success(t('common.success'))
  visible.value = false
  load()
}
async function remove(row) {
  await ElMessageBox.confirm(t('common.deleteConfirm'), t('common.confirm'), { type: 'warning' })
  await deleteUserApi(row.id)
  ElMessage.success(t('common.success'))
  load()
}
async function resetPassword(row) {
  await resetPasswordApi(row.id, { password: '123456' })
  ElMessage.success(`${t('common.success')}: 123456`)
}
onMounted(load)
</script>

