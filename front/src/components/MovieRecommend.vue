<template>
  <div class="movie-recommend container mx-auto p-6 text-white">
    <h1 class="text-3xl font-bold mb-6">영화 추천 서비스</h1>

    <form
      @submit.prevent="handleRecommend"
      class="bg-gray-800 p-6 rounded-lg shadow-lg"
    >
      <label
        for="userInput"
        class="block text-lg font-semibold text-gray-300 mb-2"
        >안녕하세요! 오늘은 어떤 영화를 찾으시나요?</label
      >
      <textarea
        id="userInput"
        v-model="userInput"
        placeholder="영화에 대한 설명을 입력하세요..."
        rows="4"
        required
        class="w-full p-4 bg-gray-700 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600 mb-4"
      ></textarea>
      <button
        :disabled="loading"
        type="submit"
        class="w-full py-3 bg-red-600 text-white text-lg rounded-lg hover:bg-red-700 disabled:bg-gray-600 transition duration-300"
      >
        {{ loading ? "추천 중..." : "추천 받기" }}
      </button>
    </form>

    <div v-if="error" class="mt-4 text-red-500">
      {{ error }}
    </div>

    <Canvas v-if="movies.length > 0" :movies="movies" class="mt-6" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import Canvas from "./Canvas.vue";

const userInput = ref("");
const movies = ref([]);
const loading = ref(false);
const error = ref("");

async function handleRecommend() {
  loading.value = true;
  error.value = "";
  movies.value = [];

  try {
    const response = await axios.post(
      "http://localhost:8000/api/v1/recommend/",
      { user_input: userInput.value }
    );

    // 응답 데이터가 빈 배열일 경우
    if (response.data.movies.length === 0) {
      error.value =
        "AI 서비스에 오류가 발생했거나 더 명확한 설명이 필요합니다. 다시 시도해주세요.";
    } else {
      movies.value = response.data.movies;
    }
  } catch (err) {
    error.value =
      err.response?.data?.error || "영화 추천 중 오류가 발생했습니다.";
    console.error("추천 오류:", err);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.movie-recommend {
  font-family: "Roboto", sans-serif;
}

form {
  background-color: #1a202c;
  padding: 20px;
  border-radius: 8px;
}

textarea {
  background-color: #2d3748;
  color: white;
  border: 1px solid #4a5568;
  border-radius: 8px;
  padding: 10px;
  font-size: 1rem;
  transition: background-color 0.3s;
}

textarea:focus {
  background-color: #4a5568;
}

button {
  background-color: #f56565;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #e53e3e;
}

button:disabled {
  background-color: #a0aec0;
}

.error {
  color: red;
  margin-top: 10px;
}

.movie-list ul {
  list-style-type: none;
  padding: 0;
}

.movie-list li {
  margin-bottom: 20px;
}
</style>
