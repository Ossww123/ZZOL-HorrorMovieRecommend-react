<!--front/src/vomponents/MovieRecommend.vue-->
<template>
  <div class="movie-recommend">
    <h1>영화 추천 서비스</h1>
    
    <form @submit.prevent="handleRecommend">
      <label for="userInput">원하는 영화 설명:</label>
      <textarea 
        id="userInput" 
        v-model="userInput" 
        placeholder="영화에 대한 설명을 입력하세요..." 
        rows="4"
        required>
      </textarea>
      <button :disabled="loading" type="submit">
        {{ loading ? "추천 중..." : "추천 받기" }}
      </button>
    </form>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="movies.length > 0" class="movie-list">
      <h2>추천 영화 목록:</h2>
      <ul>
        <li v-for="(movie, index) in movies" :key="movie.id">
          <strong>{{ index + 1 }}. {{ movie.title }}</strong>
          <p>출시일: {{ movie.release_date || "N/A" }}</p>
          <p>인기도: {{ movie.popularity }}</p>
          <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="" class="movie-image">
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// Vue 상태 관리
const userInput = ref("");
const movies = ref([]);
const loading = ref(false);
const error = ref("");

// 추천 처리 함수
async function handleRecommend() {
  loading.value = true;
  error.value = "";
  movies.value = [];

  try {
    // Django 백엔드에 영화 추천 요청
    const response = await axios.post("http://localhost:8000/api/v1/recommend/", { user_input: userInput.value });
    // 백엔드에서 받은 영화 리스트를 Vue 상태에 저장
    movies.value = response.data.movies;
  } catch (err) {
    // 오류 처리
    error.value = err.response?.data?.error || "영화 추천 중 오류가 발생했습니다.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.movie-recommend {
  font-family: Arial, sans-serif;
  padding: 20px;
}

form {
  margin-bottom: 20px;
}

textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:disabled {
  background-color: #999;
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
