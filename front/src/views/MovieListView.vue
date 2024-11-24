<template>
  <h1>전체 영화 목록 페이지</h1>

  <!-- 검색 결과가 없을 때 표시할 메시지 -->
  <div v-if="paginatedMovies.length === 0 && !isLoading" class="text-center">
    <p>일치하는 제목이 없습니다.</p>
  </div>

  <!-- 영화 목록 필터링 -->
  <div class="movie-list">
    <MovieCard
      v-for="movie in paginatedMovies"
      :key="movie.id"
      :movie="movie"
      class="movie-card"
    />
  </div>

  <!-- 로딩 중 표시 -->
  <div v-if="isLoading" class="text-center">로딩 중...</div>

  <!-- 에러 메시지 표시 -->
  <div v-if="error" class="text-center text-red-500">{{ error }}</div>

  <div class="pagination">
    <!-- 페이지 네비게이션 버튼들 -->
    <button
      @click="changePage(1)"
      :disabled="currentPage <= 1"
      class="page-button"
    >
      처음
    </button>
    <button
      @click="changePage(currentPage - 1)"
      :disabled="currentPage <= 1"
      class="page-button"
    >
      이전
    </button>
    <span>Page {{ currentPage }} of {{ totalPages }}</span>
    <button
      @click="changePage(currentPage + 1)"
      :disabled="currentPage >= totalPages"
      class="page-button"
    >
      다음
    </button>
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
import { ref, onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router"; // 검색 쿼리 처리용
import MovieCard from "@/components/MovieCard.vue";

const store = useCounterStore();
const route = useRoute();

const currentPage = ref(1); // 현재 페이지 상태 변수
const moviesPerPage = 20; // 한 페이지에 표시할 영화 수
const searchQuery = ref(route.query.search || ""); // 검색어 상태 변수
const isLoading = ref(false); // 로딩 상태
const error = ref(null); // 에러 메시지

// 전체 영화 목록 (스토어에서 가져오기)
const totalMovies = computed(() => store.movies);

// 검색어에 따라 필터링된 영화 목록
const filteredMovies = computed(() => {
  if (!searchQuery.value) {
    return totalMovies.value; // 검색어가 없으면 전체 목록 반환
  }
  return totalMovies.value.filter((movie) => {
    // 제목 또는 원제에 검색어가 포함되어 있는지 체크
    return (
      (movie.title &&
        movie.title.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (movie.original_title &&
        movie.original_title
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase()))
    );
  });
});

// 전체 페이지 수 계산 (검색어 필터링 후 전체 영화 목록 기준)
const totalPages = computed(() =>
  Math.ceil(filteredMovies.value.length / moviesPerPage)
);

// 현재 페이지에 해당하는 영화 목록 계산
const paginatedMovies = computed(() => {
  const startIndex = (currentPage.value - 1) * moviesPerPage;
  const endIndex = startIndex + moviesPerPage;
  return filteredMovies.value.slice(startIndex, endIndex);
});

// 페이지 전환 함수
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

// 영화 목록 가져오기 (스토어에서 호출)
const fetchMovies = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    await store.getMovies(); // 영화 목록 가져오기
    console.log("Movies loaded:", store.movies); // 데이터 확인
  } catch (err) {
    error.value = "영화 목록을 불러오는 중 오류가 발생했습니다.";
  } finally {
    isLoading.value = false;
  }
};

// 페이지가 처음 로드되거나 검색어가 바뀔 때마다 영화 목록을 다시 불러옵니다.
onMounted(fetchMovies);

// 검색어가 변경될 때마다 fetchMovies를 호출하여 영화 목록을 갱신
watch(searchQuery, () => {
  fetchMovies();
});

// 쿼리 파라미터(search)가 변경될 때마다 searchQuery 값을 갱신
watch(
  () => route.query.search,
  (newSearch) => {
    searchQuery.value = newSearch || ""; // 쿼리 파라미터에 search가 없다면 기본값으로 빈 문자열
    fetchMovies(); // 새로운 검색어에 맞는 영화 목록을 가져옴
  }
);
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
