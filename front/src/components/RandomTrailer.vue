<template>
  <div
    v-if="isLoading"
    class="flex justify-center items-center h-screen bg-gray-900"
  >
    <p class="text-lg text-gray-400">Loading...</p>
  </div>

  <div v-else class="container mx-auto p-6 bg-gray-900 text-white">
    <h1 class="text-center text-2xl font-bold mb-4">랜덤 영화 예고편</h1>

    <!-- 랜덤 예고편 표시 -->
    <div v-if="randomTrailer" class="flex flex-col items-center">
      <h2 class="text-xl font-semibold mb-4">{{ randomTrailer.movieTitle }}</h2>
      <iframe
        :src="'https://www.youtube.com/embed/' + randomTrailer.videoId"
        width="800"
        height="450"
        frameborder="0"
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>

    <!-- 예고편이 없을 경우 메시지 -->
    <div v-else class="text-center text-gray-400">
      <p>예고편을 찾을 수 없습니다.</p>
    </div>

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
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter"; // store 가져오기
import axios from "axios";

const store = useCounterStore();
const randomTrailer = ref(null); // 랜덤 예고편을 담을 변수
const isLoading = ref(true); // 로딩 상태

const apiKey = import.meta.env.VITE_TMDB; // TMDB API 키

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

onMounted(() => {
  getRandomTrailer(); // 페이지 로드 시 첫 랜덤 예고편 가져오기
});
</script>

<style scoped>
/* 스타일은 자유롭게 추가하세요 */
</style>
