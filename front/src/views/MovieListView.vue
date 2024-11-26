<template>
  <div :style="containerStyle" class="content-container">
    <h1 class="text-center text-4xl font-bold mb-4">전체 영화 목록 페이지</h1>

    <div v-if="paginatedMovies.length === 0 && !isLoading" class="text-center">
      <p>일치하는 제목이 없습니다.</p>
    </div>

    <div class="movie-list">
      <MovieCard
        v-for="movie in paginatedMovies"
        :key="movie.id"
        :movie="movie"
        class="movie-card"
      />
    </div>

    <div v-if="isLoading" class="text-center">로딩 중...</div>
    <div v-if="error" class="text-center text-red-500">{{ error }}</div>

    <div class="pagination">
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
  </div>
</template>

<script setup>
import { useCounterStore } from "@/stores/counter";
import { ref, onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router";
import MovieCard from "@/components/MovieCard.vue";

const store = useCounterStore();
const route = useRoute();

const currentPage = ref(1);
const moviesPerPage = 20;
const searchQuery = ref(route.query.search || "");
const isLoading = ref(false);
const error = ref(null);

const totalMovies = computed(() => store.movies);

const filteredMovies = computed(() => {
  if (!searchQuery.value) {
    return totalMovies.value;
  }
  return totalMovies.value.filter((movie) => {
    return (
      (movie.title &&
        movie.title.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (movie.original_title &&
        movie.original_title.toLowerCase().includes(searchQuery.value.toLowerCase()))
    );
  });
});

const totalPages = computed(() =>
  Math.ceil(filteredMovies.value.length / moviesPerPage)
);

const paginatedMovies = computed(() => {
  const startIndex = (currentPage.value - 1) * moviesPerPage;
  const endIndex = startIndex + moviesPerPage;
  return filteredMovies.value.slice(startIndex, endIndex);
});

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

const fetchMovies = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    await store.getMovies();
  } catch (err) {
    error.value = "영화 목록을 불러오는 중 오류가 발생했습니다.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchMovies);

watch(searchQuery, () => {
  fetchMovies();
});

watch(
  () => route.query.search,
  (newSearch) => {
    searchQuery.value = newSearch || "";
    fetchMovies();
  }
);

// Container style
const containerStyle = computed(() => {
  const width = window.innerWidth;
  let containerWidth = 1500;
  
  if (width < 1500) {
    containerWidth = width * 0.67;
  } else if (width < 1200) {
    containerWidth = width * 0.67;
  }

  const sideSpace = Math.max(width * 0.05, 20); // Calculating side space (same as in your previous code)

  return {
    maxWidth: `${containerWidth}px`,
    width: '100%',
    margin: '0 auto',
    padding: `0 ${sideSpace * 1.5}px`, // Adjusting padding for side space
  };
});
</script>

<style scoped>
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
  justify-content: center;
  align-items: center;
  width: 100%;
  min-height: 100vh;
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

h1 {
  text-align: center;
  font-size: 4rem;
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 40px;
}

/* Add padding to center content */
.content-container {
  position: relative;
  width: 100%;
  margin: 0 auto;
  /* Removing old padding here */
}
</style>
