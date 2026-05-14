<template>
  <div class="min-h-screen" style="background-color: #F5F2ED">

    <!-- Nav -->
    <nav class="px-6 py-4 flex items-center justify-between" style="background-color: #1C1C1C">
      <RouterLink to="/" style="color: #F5F2ED; font-family: Georgia, serif; font-size: 16px; text-decoration: none">
        Listas & Livros
      </RouterLink>
      <div class="flex gap-6">
        <RouterLink to="/premiacoes" class="text-sm" style="color: #9A9A8A; text-decoration: none">Premiações</RouterLink>
        <RouterLink to="/listas" class="text-sm" style="color: #9A9A8A; text-decoration: none">Listas</RouterLink>
        <RouterLink to="/livros" class="text-sm" style="color: #9A9A8A; text-decoration: none">Livros</RouterLink>
        <RouterLink to="/autores" class="text-sm" style="color: #9A9A8A; text-decoration: none">Autores</RouterLink>
      </div>
    </nav>

    <!-- Destaque -->
    <div v-if="destaqueItem" class="px-6 py-8" style="background-color: #1C1C1C">
      <p class="text-xs tracking-widest uppercase mb-2" style="color: #9A9A8A">Em destaque</p>
      <h2 class="text-2xl mb-2" style="color: #F5F2ED; font-family: Georgia, serif">{{ destaqueItem.nome || destaqueItem.titulo }}</h2>
      <p class="text-sm" style="color: #9A9A8A">{{ destaqueItem.descricao }}</p>
    </div>

    <div class="px-6 py-8 max-w-3xl mx-auto">

      <!-- Cards de ancoragem -->
      <p class="text-xs tracking-widest uppercase mb-4" style="color: #8A8880">Destaques</p>

      <div v-if="carregando" class="text-sm mb-8" style="color: #8A8880">Carregando...</div>

      <div v-else class="flex flex-col gap-4 mb-10">
        <div v-for="item in ancoragens" :key="item.id"
          class="rounded-lg overflow-hidden cursor-pointer flex"
          style="background-color: white; border: 1px solid #E0DDD7"
          @click="navegarPara(item)">
          <div class="w-24 flex-shrink-0" style="background-color: #5C6B7A; min-height: 96px"></div>
          <div class="p-4">
            <p class="text-xs tracking-widest uppercase mb-1" style="color: #8A8880">
              {{ item.tipo === 'autor' ? 'Prêmio por autor' : item._tipo === 'lista' ? 'Lista curada' : 'Premiação' }}
            </p>
            <p class="font-medium" style="color: #1C1C1C; font-family: Georgia, serif">
              {{ item.nome || item.titulo }}
            </p>
            <p class="text-sm mt-1" style="color: #8A8880">{{ item.descricao }}</p>
          </div>
        </div>
      </div>

      <!-- Últimas premiações -->
      <p class="text-xs tracking-widest uppercase mb-4" style="color: #8A8880">Últimas premiações</p>

      <div v-for="premio in premiosList" :key="premio.id" class="mb-8">
        <h3 class="text-lg mb-3 cursor-pointer" style="font-family: Georgia, serif; color: #1C1C1C"
          @click="$router.push(`/premiacoes/${premio.id}`)">
          {{ premio.nome }}
        </h3>
        <div class="flex gap-3 overflow-x-auto pb-2">
          <div v-for="livro in (livrosPorPremio[premio.id] || [])" :key="livro.id"
            class="flex-shrink-0 cursor-pointer w-28"
            @click="$router.push(`/livros/${livro.id}`)">
            <div class="rounded mb-2 flex items-end p-2"
              style="width: 112px; height: 168px; background-color: #5C6B7A">
              <span class="text-xs" style="color: rgba(255,255,255,0.85); font-family: Georgia, serif">
                {{ livro.titulo }}
              </span>
            </div>
            <p class="text-xs font-medium" style="color: #1C1C1C">{{ livro.titulo }}</p>
            <p class="text-xs" style="color: #8A8880">{{ livro.autor?.nome }}</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { livros, premios, listas } from '../services/api.js'

const router = useRouter()
const premiosList = ref([])
const livrosPorPremio = ref({})
const premiosDestaque = ref([])
const listasDestaque = ref([])
const carregando = ref(true)

const destaqueItem = computed(() => {
  const todos = [...premiosDestaque.value, ...listasDestaque.value]
  return todos.sort((a, b) => b.ordem_destaque - a.ordem_destaque)[0] || null
})

const ancoragens = computed(() => {
  const prems = premiosDestaque.value.map(p => ({ ...p, _tipo: 'premio' }))
  const lists = listasDestaque.value.map(l => ({ ...l, _tipo: 'lista' }))
  return [...prems, ...lists].sort((a, b) => a.ordem_destaque - b.ordem_destaque).slice(0, 3)
})

function navegarPara(item) {
  if (item._tipo === 'lista') {
    router.push(`/listas/${item.id}`)
  } else {
    router.push(`/premiacoes/${item.id}`)
  }
}

onMounted(async () => {
  try {
    const [premiosData, premiosDestData, listasDestData] = await Promise.all([
      premios.listar(),
      premios.destaque(),
      listas.destaque()
    ])
    premiosList.value = premiosData
    premiosDestaque.value = premiosDestData
    listasDestaque.value = listasDestData

    for (const premio of premiosData) {
      try {
        const edicoes = await premios.listarEdicoes(premio.id)
        if (edicoes.length > 0) {
          const ultimaEdicao = edicoes[edicoes.length - 1]
          const cats = await premios.listarCategorias(ultimaEdicao.id)
          let livrosEncontrados = []
          for (const cat of cats) {
            const livrosDaCat = await livros.listarPorCategoria(cat.id)
            livrosEncontrados = [...livrosEncontrados, ...livrosDaCat]
          }
          livrosPorPremio.value[premio.id] = livrosEncontrados.slice(0, 6)
        }
      } catch (e) {
        livrosPorPremio.value[premio.id] = []
      }
    }
  } catch (erro) {
    console.error('Erro ao carregar dados:', erro)
  } finally {
    carregando.value = false
  }
})
</script>