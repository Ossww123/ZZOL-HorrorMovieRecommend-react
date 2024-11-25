<template>
  <h1>보이나요</h1>

  <!-- 인기순 영화 카테고리 -->
  <div class="horror-categories">
    <h2>인기순 영화</h2>
    <div class="movie-grid">
      <div v-for="movie in popularMovies" :key="movie.id" class="movie-card" @click="saveAndNavigate(movie)">
        <img 
          :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`" 
          :alt="movie.title"
          class="movie-poster"
        >
        <div class="movie-info">
          <h3>{{ movie.title }}</h3>
          <p>평점: {{ movie.popularity }}</p>
        </div>
      </div>
    </div>
  </div>
  <hr>

  <!-- 최신순 영화 카테고리 -->
  <div class="horror-categories">
    <h2>최신순 영화</h2>
    <div class="movie-grid">
      <div v-for="movie in latestMovies" :key="movie.id" class="movie-card" @click="saveAndNavigate(movie)">
        <img 
          :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`" 
          :alt="movie.title"
          class="movie-poster"
        >
        <div class="movie-info">
          <h3>{{ movie.title }}</h3>
          <p>평점: {{ movie.release_date }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';

const store = useCounterStore()
const popularMovies = ref(null)  // store에서 인기순 영화 목록 가져오기
const latestMovies = ref(null)  // store에서 최신순 영화 목록 가져오기
const router = useRouter()

const fetchPopularMovies = async () => {
  try {
    await store.getMovieList('popularity')
    popularMovies.value = store.popularMovies
    console.log(store.popularMovies)
  } catch (error) {
    console.error('Error fetching popular movies:', error)
  }
}

const fetchLatestMovies = async () => {
  try {
    await store.getMovieList('latest')
    latestMovies.value = store.latestMovies
    console.log(store.latestMovies)
  } catch (error) {
    console.error('Error fetching latest movies:', error)
  }
}

// 영화 상세 정보를 저장하고 상세 페이지로 이동하는 함수
const saveAndNavigate = async (movie) => {
  try {
    await store.getMovieDetail(movie.id)
    router.push(`/${movie.id}`)
  } catch (error) {
    console.error('Error:', error)
  }
}


// 컴포넌트가 마운트되면 영화 데이터를 가져옴
onMounted(() => {
  fetchPopularMovies(),
  fetchLatestMovies()
})



</script>

<style scoped>
body {
  background-color: black;
  color: white; /* 텍스트 색상은 흰색으로 설정 */
  margin: 0;
  padding: 0;
}

.horror-categories {
  padding: 20px;
  background-color: black;
  color: white;
}

.category {
  margin-bottom: 40px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 15px;
}

.movie-card {
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.movie-info {
  padding: 15px;
}

.movie-info h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
}

.movie-info p {
  margin: 5px 0;
  color: #cccccc;
}
</style>
