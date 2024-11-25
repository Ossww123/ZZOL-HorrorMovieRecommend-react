<template>
  <div class="movie-card">
    <img
      :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
      alt=""
      class="movie-image"
    />
    <div class="movie-details">
      <h3>{{ movie.original_title }}</h3>
      <button @click="goDetail(movie)" class="detail-button">상세페이지</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

defineProps({
  movie: Object,
});

const goDetail = (movie) => {
  router.push(`/${movie.id}`);
};
</script>

<style scoped>
.movie-card {
  width: 200px;
  border-radius: 8px;
  overflow: hidden;
  background-color: #2d3748; /* 어두운 회색 배경 */
  color: rgb(255, 255, 255);
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* 그림자 효과 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-5px); /* 호버 시 살짝 위로 떠오르는 효과 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5); /* 강조된 그림자 */
}

.movie-image {
  width: 100%;
  height: 250px;
  object-fit: cover;
  border-bottom: 3px solid #e53e3e; /* 영화 카드 아래에 붉은 색 강조 */
}

.movie-details {
  padding: 15px;
  text-align: center;
  background-color: #2b2f3b; /* 상세 내용 배경 더 어두운 색 */
  flex-grow: 1; /* 내용 영역이 일정 비율을 차지하도록 설정 */
}

.movie-details h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e53e3e; /* 붉은색 제목 */
  margin-bottom: 10px;
  text-overflow: ellipsis; /* 텍스트가 넘칠 경우 ...으로 생략 */
  overflow: hidden; /* 텍스트 넘침 숨기기 */
  white-space: nowrap; /* 텍스트가 한 줄로만 보이도록 설정 */
  max-width: 100%; /* 제목이 넘치지 않도록 최대 너비 설정 */
}

.detail-button {
  padding: 10px 20px;
  background-color: #e53e3e; /* 붉은색 버튼 */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.detail-button:hover {
  background-color: #c53030; /* 버튼 호버 시 어두운 붉은 색 */
  transform: scale(1.05); /* 호버 시 버튼 크기 살짝 커짐 */
}

.detail-button:focus {
  outline: none; /* 포커스 시 outline 제거 */
}

@media (max-width: 768px) {
  .movie-card {
    width: 160px; /* 모바일에서 카드 크기 축소 */
  }

  .movie-details h3 {
    font-size: 1rem;
  }
}
</style>
