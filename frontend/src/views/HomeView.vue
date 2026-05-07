<template>
  <div class="min-h-screen" style="background-color: #F5F2ED">

    <!-- Navegação -->
    <nav class="px-6 py-4 flex items-center justify-between" style="background-color: #1C1C1C">
  <span class="text-lg" style="color: #F5F2ED; font-family: Georgia, serif">Listas & Livros</span>
  <div class="flex gap-6">
    <RouterLink to="/" class="text-sm no-underline" style="color: #9A9A8A">Início</RouterLink>
    <RouterLink to="/" class="text-sm no-underline" style="color: #9A9A8A">Premiações</RouterLink>
    <RouterLink to="/" class="text-sm no-underline" style="color: #9A9A8A">Listas</RouterLink>
  </div>
</nav>

    <!-- Conteúdo -->
    <div class="px-6 py-8 max-w-5xl mx-auto">

      <!-- Seção de premiações -->
      <p class="text-xs tracking-widest uppercase mb-2" style="color: #8A8880">Premiações em destaque</p>
      <h2 class="text-xl mb-4" style="font-family: Georgia, serif; color: #1C1C1C">Prêmios literários</h2>

      <div v-if="carregando" class="text-sm" style="color: #8A8880">Carregando...</div>

      <div v-else>
        <div v-if="premiosList.length === 0" class="text-sm" style="color: #8A8880">
          Nenhum prêmio cadastrado ainda.
        </div>
        <div v-for="premio in premiosList" :key="premio.id"
          class="rounded-lg p-5 mb-4 cursor-pointer" style="background-color: #1C1C1C">
          <p class="mb-1" style="color: #F5F2ED; font-family: Georgia, serif; font-size: 18px">{{ premio.nome }}</p>
          <p class="text-sm" style="color: #9A9A8A">{{ premio.descricao }}</p>
        </div>
      </div>

      <!-- Seção de listas -->
      <p class="text-xs tracking-widest uppercase mb-2 mt-8" style="color: #8A8880">Listas curadas</p>
      <h2 class="text-xl mb-4" style="font-family: Georgia, serif; color: #1C1C1C">Os mais lidos</h2>

      <div v-if="livrosList.length === 0 && !carregando" class="text-sm" style="color: #8A8880">
        Nenhum livro cadastrado ainda.
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="livro in livrosList" :key="livro.id"
          class="cursor-pointer" @click="$router.push(`/livros/${livro.id}`)">
          <div class="w-full rounded mb-2 flex items-end p-2"
            style="aspect-ratio: 2/3; background-color: #5C6B7A">
            <span class="text-xs" style="color: rgba(255,255,255,0.85); font-family: Georgia, serif">{{ livro.titulo }}</span>
          </div>
          <p class="text-sm font-medium" style="color: #1C1C1C">{{ livro.titulo }}</p>
          <p class="text-xs" style="color: #8A8880">{{ livro.autor?.nome }}</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { livros, premios } from '../services/api.js'

const livrosList = ref([])
const premiosList = ref([])
const carregando = ref(true)

onMounted(async () => {
  try {
    const [livrosData, premiosData] = await Promise.all([
      livros.listar(),
      premios.listar()
    ])
    livrosList.value = livrosData
    premiosList.value = premiosData
  } catch (erro) {
    console.error('Erro ao carregar dados:', erro)
  } finally {
    carregando.value = false
  }
})
</script>