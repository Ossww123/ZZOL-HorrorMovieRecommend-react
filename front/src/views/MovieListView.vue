<template>
  <h1>전체 영화 목록 페이지</h1>

  <!-- 영화 목록 필터링 -->
  <div class="movie-list">
    <MovieCard
      v-for="movie in paginatedMovies"
      :key="movie.id"
      :movie="movie"
      class="movie-card"
    />
  </div>

  <div class="pagination">
    <!-- 첫 페이지로 이동 버튼 -->
    <button
      @click="changePage(1)"
      :disabled="currentPage <= 1"
      class="page-button"
    >
      처음
    </button>

    <!-- 이전 페이지로 이동 버튼 -->
    <button
      @click="changePage(currentPage - 1)"
      :disabled="currentPage <= 1"
      class="page-button"
    >
      이전
    </button>

    <span>Page {{ currentPage }} of {{ totalPages }}</span>

    <!-- 다음 페이지로 이동 버튼 -->
    <button
      @click="changePage(currentPage + 1)"
      :disabled="currentPage >= totalPages"
      class="page-button"
    >
      다음
    </button>

    <!-- 마지막 페이지로 이동 버튼 -->
    <button
      @click="changePage(totalPages)"
      :disabled="currentPage >= totalPages"
      class="page-button"
    >
      끝
    </button>
  </div>
</template>

<script setup>
import { useCounterStore } from "@/stores/counter";
import { ref, onMounted, computed } from "vue";
import MovieCard from "@/components/MovieCard.vue";

const store = useCounterStore();
const currentPage = ref(1); // 현재 페이지 상태 변수
const moviesPerPage = 20; // 한 페이지에 표시할 영화 수

// 전체 영화 목록
const totalMovies = computed(() => store.movies);

// 전체 페이지 수 계산 (전체 영화 목록 기준)
const totalPages = computed(() =>
  Math.ceil(totalMovies.value.length / moviesPerPage)
);

// 현재 페이지에 해당하는 영화 목록 계산
const paginatedMovies = computed(() => {
  const startIndex = (currentPage.value - 1) * moviesPerPage;
  const endIndex = startIndex + moviesPerPage;
  return totalMovies.value.slice(startIndex, endIndex);
});

// 페이지 전환 함수
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

onMounted(() => {
  store.getMovies(); // 영화 목록 가져오기
});
</script>

<style scoped>
/* 배경을 검정색으로 설정 */
body {
  background-color: black;
  color: white;
  margin: 0;
  padding: 0;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  width: 100%;
  min-height: 100vh; /* 화면 최소 높이를 100vh로 설정하여 수직 정렬이 잘 되도록 함 */
}

.movie-card {
  width: 200px;
  padding: 15px;
  flex-shrink: 0;
  border: 1px solid #000;
  background-color: #2d3748;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

.movie-image {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.movie-details {
  text-align: center;
  flex-grow: 1;
  overflow: hidden;
}

/* 페이지 네비게이션 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.page-button {
  background-color: #333;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  cursor: pointer;
  border-radius: 4px;
}

.page-button:disabled {
  background-color: #666;
  cursor: not-allowed;
}
</style>
