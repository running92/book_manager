<template>
  <el-container class="app-shell">
    <el-aside width="232px" class="sidebar">
      <div class="brand">
        <el-icon><Reading /></el-icon>
        <span>{{ t('app.name') }}</span>
      </div>
      <el-menu :default-active="route.path" router background-color="#111827" text-color="#cbd5e1" active-text-color="#ffffff">
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ t(item.title) }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="topbar">
        <div class="page-title">{{ t(route.meta.title || 'menu.dashboard') }}</div>
        <div class="top-actions">
          <el-button-group>
            <el-button :type="locale === 'zh-CN' ? 'primary' : 'default'" @click="setLang('zh-CN')">中文</el-button>
            <el-button :type="locale === 'en-US' ? 'primary' : 'default'" @click="setLang('en-US')">EN</el-button>
          </el-button-group>
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              {{ auth.user?.real_name }} <el-tag size="small">{{ auth.user?.role === 'admin' ? t('app.admin') : t('app.reader') }}</el-tag>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">{{ t('menu.profile') }}</el-dropdown-item>
                <el-dropdown-item command="logout" divided>Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useAppStore } from '../store/app'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const app = useAppStore()
const locale = computed(() => app.locale)

const allMenus = [
  { path: '/dashboard', title: 'menu.dashboard', icon: 'DataBoard' },
  { path: '/books', title: 'menu.books', icon: 'Collection' },
  { path: '/categories', title: 'menu.categories', icon: 'Folder', roles: ['admin'] },
  { path: '/users', title: 'menu.users', icon: 'User', roles: ['admin'] },
  { path: '/borrow', title: 'menu.borrow', icon: 'Tickets', roles: ['admin'] },
  { path: '/my-borrow', title: 'menu.myBorrow', icon: 'Notebook' },
  { path: '/profile', title: 'menu.profile', icon: 'Setting' }
]

const menus = computed(() => allMenus.filter(item => !item.roles || item.roles.includes(auth.user?.role)))

function setLang(lang) {
  app.setLocale(lang)
}

function handleCommand(command) {
  if (command === 'profile') router.push('/profile')
  if (command === 'logout') {
    auth.logout()
    router.replace('/login')
  }
}
</script>

