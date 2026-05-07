const BASE_URL = 'http://localhost:8000'

async function request(path, options = {}) {
  const resposta = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  })

  if (!resposta.ok) {
    throw new Error(`Erro ${resposta.status}: ${resposta.statusText}`)
  }

  if (resposta.status === 204) return null

  return resposta.json()
}

export const livros = {
  listar: () => request('/livros/'),
  buscar: (id) => request(`/livros/${id}`),
}

export const autores = {
  listar: () => request('/autores/'),
  buscar: (id) => request(`/autores/${id}`),
}

export const premios = {
  listar: () => request('/premios/'),
  buscar: (id) => request(`/premios/${id}`),
  listarEdicoes: (premioId) => request(`/premios/${premioId}/edicoes`),
  listarCategorias: (edicaoId) => request(`/premios/edicoes/${edicaoId}/categorias`),
}

export const listas = {
  listar: () => request('/listas/'),
  buscar: (id) => request(`/listas/${id}`),
  listarLivros: (listaId) => request(`/listas/${listaId}/livros`),
}