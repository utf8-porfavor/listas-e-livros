import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LivroView from '../views/LivroView.vue'
import PremiacaoView from '../views/PremiacaoView.vue'
import ListaView from '../views/ListaView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/livros/:id',
      name: 'livro',
      component: LivroView
    },
    {
      path: '/premiacoes/:id',
      name: 'premiacao',
      component: PremiacaoView
    },
    {
      path: '/listas/:id',
      name: 'lista',
      component: ListaView
    },
  ],
})

export default router