<template>
  <div class="main-container" @mousemove="moveImage">
    <!-- 좌측 움직이는 이미지 -->
    <img
      src="@/assets/ghost1.png"
      alt="Left Ghost"
      :style="{
        transform: `translate(${imagePosition1.x}px, ${imagePosition1.y}px)`,
        width: `${imageWidth}vw`,
        left: `${sideSpace}px`
      }"
      class="absolute z-10"
    />

    <!-- 우측 움직이는 이미지 -->
    <img
      src="@/assets/ghost2.png"
      alt="Right Ghost"
      :style="{
        transform: `translate(${imagePosition2.x}px, ${imagePosition2.y}px)`,
        width: `${imageWidth}vw`,
        right: `${sideSpace}px`
      }"
      class="absolute z-10"
    />

    <!-- 좌측 움직이는 이미지 -->
    <img
      src="@/assets/ghost2.png"
      alt="Left Ghost"
      :style="{
        transform: `translate(${imagePosition3.x}px, ${imagePosition3.y}px)`,
        width: `${imageWidth}vw`,
        left: `${sideSpace}px`
      }"
      class="absolute z-10"
    />

    <!-- 우측 움직이는 이미지 -->
    <img
      src="@/assets/ghost1.png"
      alt="Right Ghost"
      :style="{
        transform: `translate(${imagePosition4.x}px, ${imagePosition4.y}px)`,
        width: `${imageWidth}vw`,
        right: `${sideSpace}px`
      }"
      class="absolute z-10"
    />

    <!-- 중앙에 배치된 콘텐츠를 감싸는 컨테이너 -->
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
  </div>
</template>

<script setup>
import { useCounterStore } from "@/stores/counter";
import { ref, onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router";
import MovieCard from "@/components/MovieCard.vue";

// 상태 변수 정의
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

// 움직이는 이미지 관련 상태 및 함수
const imagePosition1 = ref({ x: 0, y: 0 });
const imagePosition2 = ref({ x: 0, y: 0 });
const imagePosition3 = ref({ x: 0, y: 0 });
const imagePosition4 = ref({ x: 0, y: 0 });
const imageWidth = ref(10);

const sideSpace = computed(() => {
  const width = window.innerWidth;
  return Math.max(width * 0.05, 20); // 최소 20px, 화면 너비의 5%
});

// 이미지 크기 조정 함수
const updateImageSize = () => {
  const width = window.innerWidth;
  imageWidth.value = Math.min(width * 0.08, 10); // 최대 10vw, 화면 너비의 8%
};

// 화면 크기에 따라 이미지 크기 변경
window.addEventListener('resize', () => {
  updateImageSize();
});
updateImageSize();

// 마우스 이동에 따라 이미지 위치 변경
const moveImage = (event) => {
  const { clientX, clientY } = event;
  const scrollY = window.scrollY;

  const maxMove = window.innerWidth * 0.05; // 최대 이동 거리

  // 왼쪽 이미지
  const leftX = ((clientX - window.innerWidth / 2) / 15) - window.innerWidth / 20;
  imagePosition1.value.x = Math.min(Math.max(leftX, -maxMove), maxMove);
  imagePosition3.value.x = Math.min(Math.max(leftX, -maxMove), maxMove);

  // 오른쪽 이미지
  const rightX = ((clientX - window.innerWidth / 2) / 15) + window.innerWidth / 20;
  imagePosition2.value.x = Math.min(Math.max(rightX, -maxMove), maxMove);
  imagePosition4.value.x = Math.min(Math.max(rightX, -maxMove), maxMove);

  // y 위치
  imagePosition1.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight/10;
  imagePosition2.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight/10;
  imagePosition3.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight/2;
  imagePosition4.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight/2;
};
</script>

<style scoped>
.main-container {
  position: relative;
  min-height: 100vh;
  background-color: black;
  width: 100%;
  height: 100%;
}

img {
  transition: transform 0.1s ease-out;
}

.content-container {
  position: relative;
  width: 100%;
  margin: 0 auto;
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
</style>
