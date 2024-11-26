<template>
  <div class="create-article-container text-white min-h-screen flex flex-col items-center py-12">
    <h1 class="text-4xl font-bold text-red-500 mb-8">게시글 작성</h1>
    <form @submit.prevent="createArticle" class="w-full max-w-xl bg-gray-800 p-8 rounded-lg shadow-lg">
      <div class="mb-6">
        <label for="title" class="block text-lg mb-2">제목 :</label>
        <input 
          type="text" 
          id="title" 
          v-model.trim="title" 
          class="w-full p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-red-500"
        />
      </div>
      <div class="mb-6">
        <label for="content" class="block text-lg mb-2">내용 :</label>
        <textarea 
          id="content" 
          v-model.trim="content" 
          class="w-full p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-red-500"
        ></textarea>
      </div>
      <button 
        type="submit"
        class="w-full py-3 bg-red-600 text-white font-bold rounded-lg shadow-lg hover:bg-red-700 transition duration-300"
      >
        게시글 작성
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { useRouter } from 'vue-router'

const title = ref('')
const content = ref('')
const store = useCounterStore()
const router = useRouter()

const createArticle = async () => {
  try {
    await axios.post(`${store.API_URL}/api/v1/articles/`, {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    router.push({ name: 'ArticleView' })
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
/* .create-article-container {
  background-color: #1a202c;
} */

form input, form textarea {
  font-size: 1rem;
}
</style>
