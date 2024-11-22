<template>
  <h1>전체 영화 목록 페이지</h1>
  <div class="movie-list">
    <MovieCard
      v-for="movie in store.movies"
      :key="movie.id"
      :movie="movie"
      class="movie-card"
    />
  </div>
</template>

<script setup>
  import { useCounterStore } from '@/stores/counter'
  import { onMounted } from 'vue'
  import MovieCard from '@/components/MovieCard.vue';

  const store = useCounterStore();

  onMounted(() => {
    store.getMovies();
    console.log(store.movies);
    console.log('여기는 됬냐?');
  });
</script>

<style scoped>
/* 배경을 검정색으로 설정 */
body {
  background-color: black;
  color: white; /* 텍스트 색상은 흰색으로 설정 */
  margin: 0;
  padding: 0;
}

.movie-list {
  display: flex;
  gap: 20px;
  position: relative;
  width: 100%;  /* 부모 컨테이너에 맞춰 크기 설정 */
  animation: scrollMovies 20s linear infinite;  /* 자동 스크롤 애니메이션 */
}

/* 영화 카드 스타일 */
.movie-card {
  width: 200px;
  padding: 15px;
  flex-shrink: 0;  /* 카드가 줄어들지 않도록 */
  border: 1px solid #000;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  /* height: 350px;  이 부분을 제거하여 높이가 자동으로 조정되도록 함 */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 카드 내 콘텐츠를 위아래로 정렬 */
  overflow: hidden; /* 내용이 넘칠 경우 숨기기 */
}

.movie-image {
  width: 100%;
  max-height: 200px; /* 이미지 최대 높이 제한 */
  object-fit: cover; /* 이미지를 잘라서 카드에 맞게 표시 */
  border-radius: 4px;
}

.movie-details {
  text-align: center;
  flex-grow: 1; /* 카드 내 세부 사항이 남은 공간을 차지하도록 함 */
  overflow: hidden; /* 내용이 넘칠 경우 숨기기 */
}

@keyframes scrollMovies {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-100%);  /* 전체 영화 목록이 왼쪽으로 이동 */
  }
}
</style>
