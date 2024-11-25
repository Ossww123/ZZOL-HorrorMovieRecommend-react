<template>
  <!-- 인기순 영화 카테고리 -->
  <div class="horror-categories">
    <h2>인기순 영화</h2>
    <div class="slider-container">
      <button
        class="slide-button prev"
        @click="slide('prev', 'popular')"
        :disabled="currentIndexes['popular'] === 0"
      >
        &#10094;
      </button>

      <div class="slider-wrapper">
        <div
          class="movie-slider"
          :style="{
            transform: `translateX(-${currentIndexes['popular'] * 100}%)`,
          }"
        >
          <div
            v-for="movie in popularMovies"
            :key="movie.id"
            class="movie-card-wrapper"
          >
            <div class="movie-card" @click="saveAndNavigate(movie)">
              <div class="movie-poster-wrapper">
                <img
                  :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
                  :alt="movie.title"
                  class="movie-poster"
                />
              </div>
              <div class="movie-info">
                <h3>{{ movie.title }}</h3>
                <p>평점: {{ movie.vote_average }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <button
        class="slide-button next"
        @click="slide('next', 'popular')"
        :disabled="
          currentIndexes['popular'] >= popularMovies.length - itemsToShow
        "
      >
        &#10095;
      </button>
    </div>
  </div>

  <!-- 최신순 영화 카테고리 -->
  <div class="horror-categories">
    <h2>최신순 영화</h2>
    <div class="slider-container">
      <button
        class="slide-button prev"
        @click="slide('prev', 'latest')"
        :disabled="currentIndexes['latest'] === 0"
      >
        &#10094;
      </button>

      <div class="slider-wrapper">
        <div
          class="movie-slider"
          :style="{
            transform: `translateX(-${currentIndexes['latest'] * 100}%)`,
          }"
        >
          <div
            v-for="movie in latestMovies"
            :key="movie.id"
            class="movie-card-wrapper"
          >
            <div class="movie-card" @click="saveAndNavigate(movie)">
              <div class="movie-poster-wrapper">
                <img
                  :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
                  :alt="movie.title"
                  class="movie-poster"
                />
              </div>
              <div class="movie-info">
                <h3>{{ movie.title }}</h3>
                <p>평점: {{ movie.vote_average }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button
        class="slide-button next"
        @click="slide('next', 'latest')"
        :disabled="
          currentIndexes['latest'] >= latestMovies.length - itemsToShow
        "
      >
        &#10095;
      </button>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from "@/stores/counter";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const store = useCounterStore();
const popularMovies = ref([]); // store에서 인기순 영화 목록 가져오기
const latestMovies = ref([]); // store에서 최신순 영화 목록 가져오기
const currentIndexes = ref({ popular: 0, latest: 0 }); // 각 카테고리의 현재 인덱스
const itemsToShow = 4; // 한 번에 보여줄 영화 수
const router = useRouter();

const fetchPopularMovies = async () => {
  try {
    await store.getMovieList("popularity");
    popularMovies.value = store.popularMovies;
    console.log("popular", store.popularMovies);
  } catch (error) {
    console.error("Error fetching popular movies:", error);
  }
};

const fetchLatestMovies = async () => {
  try {
    await store.getMovieList("latest");
    latestMovies.value = store.latestMovies;
    console.log("latest", store.latestMovies);
  } catch (error) {
    console.error("Error fetching latest movies:", error);
  }
};

// 영화 상세 정보를 저장하고 상세 페이지로 이동하는 함수
const saveAndNavigate = async (movie) => {
  try {
    await store.getMovieDetail(movie.id);
    router.push(`/${movie.id}`);
  } catch (error) {
    console.error("Error:", error);
  }
};

// 슬라이드를 이동하는 함수
const slide = (direction, category) => {
  if (direction === "next") {
    currentIndexes.value[category] = Math.min(
      currentIndexes.value[category] + 1,
      category === "popular"
        ? popularMovies.value.length - itemsToShow
        : latestMovies.value.length - itemsToShow
    );
  } else {
    currentIndexes.value[category] = Math.max(
      currentIndexes.value[category] - 1,
      0
    );
  }
};

// 컴포넌트가 마운트되면 영화 데이터를 가져옴
onMounted(() => {
  console.log("?????????????????????????????????????????????");
  fetchPopularMovies();
  fetchLatestMovies();
});
</script>

<style scoped>
h2 {
  font-weight: bold; /* 볼드 효과 */
}

body {
  background-color: black;
  color: white;
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

.slider-container {
  position: relative;
  width: 100%;
  padding: 0 40px;
}

.slider-wrapper {
  overflow: hidden;
}

.movie-slider {
  display: flex;
  transition: transform 0.5s ease;
  gap: 20px;
}

.movie-card-wrapper {
  flex: 0 0 calc((100% - (20px * 3)) / 4); /* 4개의 카드와 3개의 gap을 고려한 계산 */
  width: 250px; /* 카드의 기본 너비 설정 */
}

.movie-card {
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  width: 100%;
  height: 100%;
  transition: transform 0.3s;
  display: flex;
  flex-direction: column;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.movie-poster-wrapper {
  position: relative;
  width: 100%;
  padding-top: 150%; /* 2:3 비율 유지 */
  overflow: hidden;
}

.movie-poster {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 이미지 비율 유지하면서 영역 채우기 */
}

.movie-info {
  padding: 15px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #1a1a1a;
}

.movie-info h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 최대 2줄까지만 표시 */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.movie-info p {
  margin: 5px 0;
  color: #cccccc;
}

.slide-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 15px;
  cursor: pointer;
  z-index: 10;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.prev {
  left: 10px;
}

.next {
  right: 10px;
}

@media (max-width: 1024px) {
  .movie-card-wrapper {
    flex: 0 0 calc((100% - (20px * 2)) / 3); /* 3개의 카드와 2개의 gap */
  }
}

@media (max-width: 768px) {
  .movie-card-wrapper {
    flex: 0 0 calc((100% - 20px) / 2); /* 2개의 카드와 1개의 gap */
  }
}

@media (max-width: 480px) {
  .movie-card-wrapper {
    flex: 0 0 100%; /* 1개의 카드 */
  }
}
</style>
