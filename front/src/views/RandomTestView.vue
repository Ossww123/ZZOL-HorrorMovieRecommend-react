<template>
    <h1>보이나요</h1>
    <div class="horror-categories">
      <div v-if="randomMovies" v-for="(movies, category) in randomMovies" :key="category" class="category">
        <h2>오늘은 "{{ category }}"!</h2>
        <div class="movie-grid">
          <div v-for="movie in movies" :key="movie.id" class="movie-card">
            <img 
              :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`" 
              :alt="movie.title"
              class="movie-poster"
            >
            <div class="movie-info">
              <h3>{{ movie.title }}</h3>
              <p>평점: {{ movie.vote_average }}</p>
            </div>
          </div>
        </div>
      </div>
      <hr>
    </div>
  </template>
  
  <script setup>
  import { useCounterStore } from '@/stores/counter'
  import { ref, onMounted } from 'vue'
  
  const store = useCounterStore()
  const randomMovies = ref(null)
  
  const fetchRandomMovies = async () => {
    try {
      const response = await store.getRandomMovies()
      randomMovies.value = response
      console.log(randomMovies.value)
    } catch (error) {
      console.error('Error fetching random movies:', error)
    }
  }
  
  onMounted(() => {
    fetchRandomMovies()
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