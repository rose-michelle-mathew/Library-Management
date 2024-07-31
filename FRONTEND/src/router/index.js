import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LogoutView from '../views/LogoutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')

    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/add_book',
      name: 'addBook',
      component: () => import('../views/AddBook.vue')
    },
    {
      path: '/view_books',
      name: 'ViewBooks',
      component: () => import('../views/ViewBooks.vue')
    },
    {
      path: '/add_section',
      name: 'AddSection',
      component: () => import('../views/AddSection.vue')
    },
    {
      path: '/Sections',
      name: 'Sections',
      component: () => import('../components/Sections.vue')
    },
    {
      path: '/requests',
      name: 'Requests',
      component: () => import('../views/Requests.vue')
    },
    {
      path: '/borrowed',
      name: 'Borrowed',
      component: () => import('../views/BorrowedBooks.vue')
    },
    {
      path: '/history',
      name: 'History',
      component: () => import('../views/History.vue')
    }
  ]
})

export default router
