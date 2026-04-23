import { defineStore } from 'pinia'
import i18n from '../locales'

export const useAppStore = defineStore('app', {
  state: () => ({
    locale: localStorage.getItem('locale') || 'zh-CN'
  }),
  actions: {
    setLocale(locale) {
      this.locale = locale
      localStorage.setItem('locale', locale)
      i18n.global.locale.value = locale
      document.documentElement.lang = locale
    }
  }
})

