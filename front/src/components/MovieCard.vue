<template>
  <div class="movie-card">
    <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="" class="movie-image">
    <div class="movie-details">
      <h3>{{ movie.original_title }}</h3>
      <!-- <p>{{ movie.overview }}</p> -->
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
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.movie-card {
  border: 1px solid #000;
  width: 200px;
  padding: 15px;
  background-color: #666666; /* 회색 배경 */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 세부 사항을 하단으로 배치 */
}

.movie-image {
  width: 100%;
  height: 250px; /* 고정 높이로 설정 */
  object-fit: cover; /* 이미지가 카드 크기에 맞게 잘림 */
  border-radius: 4px; /* 이미지 모서리 둥글게 */
}

.movie-details {
  text-align: center;
  color: #000;
}
</style>
