<template>
  <div>
    <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="" class="movie-image">
      <div class="movie-details">
        <h3>{{  movie.original_title }}</h3>
        <p>{{ movie.overview }}</p>
        <button @click="goDetail(movie)">상세페이지로 이동</button>
      </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter();

defineProps({
  movie: Object
})
  const goDetail = (movie) => {
    router.push(`/${movie.id}`)
}
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