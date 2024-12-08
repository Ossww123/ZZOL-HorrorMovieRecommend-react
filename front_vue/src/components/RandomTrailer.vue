<template>
  <div
    v-if="isLoading"
    class="flex justify-center items-center h-screen bg-gray-900"
  >
    <p class="text-lg text-gray-400">Loading...</p>
  </div>

  <div v-else class="container mx-auto p-6 text-white">
    <h1 class="text-center text-2xl font-bold mb-4">랜덤 영화 예고편</h1>

    <!-- 랜덤 예고편 표시 -->
    <transition
      name="slide-fade"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <div v-show="randomTrailer" class="flex flex-col items-center">
        <h2 class="text-xl font-semibold mb-4">
          {{ randomTrailer.movieTitle }}
        </h2>
        <RouterLink :to="`/random/${randomTrailer.id}`">
            {{ randomTrailer.movieTitle }}
        </RouterLink>
        <iframe
          :src="'https://www.youtube.com/embed/' + randomTrailer.videoId"
          width="800"
          height="450"
          frameborder="0"
          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </transition>

    <!-- 예고편이 없을 경우 메시지 -->
    <transition
      name="slide-fade"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <div v-show="!randomTrailer" class="text-center text-gray-400">
        <p>예고편을 찾을 수 없습니다.</p>
      </div>
    </transition>

    <!-- "다음" 버튼 -->
    <div class="text-center mt-6">
      <button
        @click="getRandomTrailer"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700 transition duration-300"
      >
        다음 예고편
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from "vue";
import { useCounterStore } from "@/stores/counter"; // store 가져오기
import axios from "axios";
import { random } from "lodash";
import { useRouter } from "vue-router";

const store = useCounterStore();
const randomTrailer = ref(null); // 랜덤 예고편을 담을 변수
const isLoading = ref(true); // 로딩 상태
const movie = ref([])
const apiKey = import.meta.env.VITE_TMDB; // TMDB API 키
const router = useRouter()

// 영화 목록에서 랜덤 예고편을 가져오는 함수
const getRandomTrailer = async () => {
  // 영화 목록을 가져옵니다.
  const movies = store.movies;
  if (movies.length === 0) return;

  // 랜덤으로 영화 하나 선택
  const randomMovie = movies[Math.floor(Math.random() * movies.length)];
  
  try {
    // TMDB API에서 해당 영화의 예고편 정보 가져오기
    const response = await axios.get(
      `https://api.themoviedb.org/3/movie/${randomMovie.tmdb_Id}/videos?api_key=${apiKey}`
    );

    const trailers = response.data.results;

    // 예고편이 있을 경우, 랜덤으로 예고편 하나 선택
    if (trailers.length > 0) {
      const randomTrailerData =
        trailers[Math.floor(Math.random() * trailers.length)];
      
      // YouTube 영상 ID로 예고편 정보 설정
      randomTrailer.value = {
        id: randomMovie.tmdb_Id,
        movieTitle: randomMovie.title,
        videoId: randomTrailerData.key,
      };
    } else {
      randomTrailer.value = null; // 예고편이 없을 경우 null 처리
    }
  } catch (error) {
    console.error("예고편을 가져오는 데 실패했습니다.", error);
    randomTrailer.value = null; // 예고편 로딩 실패 시 null 처리
  } finally {
    isLoading.value = false; // 로딩 완료
  }
};

// 오른쪽 방향키로 다음 예고편을 불러오는 이벤트 리스너
const handleKeyDown = (event) => {
  if (event.key === "ArrowRight") {
    getRandomTrailer(); // 오른쪽 방향키가 눌리면 getRandomTrailer 실행
  }
};

onMounted(() => {
  getRandomTrailer(); // 페이지 로드 시 첫 랜덤 예고편 가져오기
  window.addEventListener("keydown", handleKeyDown); // keydown 이벤트 리스너 추가
});
// 컴포넌트가 언마운트될 때 이벤트 리스너 제거
onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleKeyDown);
});

const goDetail = (movie) => {
  router.push(`/random/${movie.id}`);
};


</script>

<style scoped>
/* 슬라이드 애니메이션 설정 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.slide-fade-enter,
.slide-fade-leave-to /* .slide-fade-leave-active in <2.1.8 */ {
  transform: translateX(100%);
  opacity: 0;
}

.slide-fade-enter-to,
.slide-fade-leave {
  transform: translateX(0);
  opacity: 1;
}
</style>
