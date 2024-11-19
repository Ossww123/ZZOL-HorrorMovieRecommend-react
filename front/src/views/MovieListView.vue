<template>
  <h1>전체 영화 목록 페이지</h1>
  <div class="movie-list">
     <MovieCard
     v-for="movie in store.movies"
      :key="movie.id"
      :movie="movie"
      class="movie-card"/> 
    </div>
</template>

<script setup>
  import { useCounterStore } from '@/stores/counter'
  
  import { onMounted } from 'vue'
  import MovieCard from '@/components/MovieCard.vue';

  const store = useCounterStore();
  

  onMounted(() => {
    store.getMovies();
  })

  
</script>

<style scoped>
.movie-list{
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.movie-card {
  border: 1px solid #000;
  width: 200px;
  padding: 15px;
}

.movie-image{
  width: 100%;
}

.movie-details{
  text-align: center;
}
</style>