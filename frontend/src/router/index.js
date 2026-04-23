import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('../layout/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('../views/DashboardView.vue'), meta: { title: 'menu.dashboard' } },
      { path: 'books', name: 'Books', component: () => import('../views/BooksView.vue'), meta: { title: 'menu.books' } },
      { path: 'books/:id', name: 'BookDetail', component: () => import('../views/BookDetailView.vue'), meta: { title: 'common.detail' } },
      { path: 'categories', name: 'Categories', component: () => import('../views/CategoriesView.vue'), meta: { title: 'menu.categories', roles: ['admin'] } },
      { path: 'users', name: 'Users', component: () => import('../views/UsersView.vue'), meta: { title: 'menu.users', roles: ['admin'] } },
      { path: 'borrow', name: 'BorrowRecords', component: () => import('../views/BorrowRecordsView.vue'), meta: { title: 'menu.borrow', roles: ['admin'] } },
      { path: 'my-borrow', name: 'MyBorrow', component: () => import('../views/MyBorrowView.vue'), meta: { title: 'menu.myBorrow' } },
      { path: 'profile', name: 'Profile', component: () => import('../views/ProfileView.vue'), meta: { title: 'menu.profile' } }
    ]
  },
  { path: '/:pathMatch(.*)*', component: () => import('../views/NotFoundView.vue') }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.meta.public) return auth.isLogin ? '/dashboard' : true
  if (!auth.isLogin) return '/login'
  if (!auth.user) await auth.fetchMe()
  if (to.meta.roles && !to.meta.roles.includes(auth.user?.role)) return '/dashboard'
  return true
})

export default router

