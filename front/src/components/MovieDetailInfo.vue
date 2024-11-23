<!--MovieDetailInfo.vue-->
<template>
  <div v-if="movie">
    <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="" class="movie-image">
    <img :src="'https://image.tmdb.org/t/p/w500' + movie.backdrop_path" alt="" class="movie-image">
    <h3>{{  movie.title }}</h3>
    <p>개봉일: {{  movie.release_date }}</p>
    <p>러닝타임: {{ runtime.runtime }}분</p>
    <p>TMDB 평점: {{ movie.tmdb_vote_sum }} </p>
    <h3>장르</h3>
    <!-- <p>장르 : {{ getGenres(movie.genre_ids) }}</p> -->
    <h3>줄거리</h3>
    <p>{{ movie.overview }}</p>
    <h3>공식 예고편</h3>
    <button @click="openTrailerModal">예고편 보기</button>
    <h3>키워드</h3>
    <p v-for="keyword in keywords.keywords">{{ keyword.name }}</p>
    <p>{{ movie.user_vote_sum }}  ({{ movie.user_vote_cnt }})</p>
    <p>{{ movie.fear_index }}</p>
    <YoutubeTrailerModal
      v-if="isModalVisible"
      :showModal="isModalVisible"
      :movie="movie"
      @close="closeTrailerModal"
    />

  </div>
  <div v-else-if="isLoading">
    <p>Loading...</p>
  </div>
  <div v-else>
    <p>영화를 찾을 수 없습니다.</p>
  </div>
  <MovieDetailReview
  :movie_pk="movieId"
  @reviewCreated="updateMovieData"
  />
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter';
import { onMounted, computed, ref } from 'vue'
import YoutubeTrailerModal from './YoutubeTrailerModal.vue';
import MovieDetailReview from '@/components/MovieDetailReview.vue';


const store = useCounterStore();
const route = useRoute();
const movieId = route.params.movie_id;
const apiKey = import.meta.env.VITE_TMDB;
const movie = ref(null)

const isLoading = ref(true)
const isModalVisible = ref(false) // 모달의 열림 상태
const runtime = ref([])
const keywords = ref([])

import axios from 'axios';

// 영화 러닝타임을 가져오는 함수
const getMovieRuntime = async (movieId) => {
    const response = await axios.get(
      `https://api.themoviedb.org/3/movie/${movieId}?api_key=${apiKey}` 
    ).then((res) => {
      console.log("222222222까지오나")
      console.log(res.data)
      runtime.value = res.data
      console.log(runtime.value)
    })
    .catch((err) => {
      console.log("아님여긴가2222222")
      console.log(err)
    })
  }
  // catch (error) {
  //   console.error('영화 러닝타임을 가져오는 데 실패했습니다:', error);
  //   runtime.value = '정보 없음';
  // }

const getKeyword = async (movieId) => {
  const response = await axios.get(
      `https://api.themoviedb.org/3/movie/${movieId}/keywords?api_key=${apiKey}`
    );
    console.log('여기에요')
    keywords.value = response.data
    console.log(keywords.value)
}



const genreList = [
  { "id": 28, "name": "액션" },
  { "id": 12, "name": "모험" },
  { "id": 16, "name": "애니메이션" },
  { "id": 35, "name": "코미디" },
  { "id": 80, "name": "범죄" },
  { "id": 99, "name": "다큐멘터리" },
  { "id": 18, "name": "드라마" },
  { "id": 27, "name": "공포" },
  { "id": 10749, "name": "로맨스" },
  { "id": 878, "name": "SF" },
  { "id": 53, "name": "스릴러" },
  { "id": 10752, "name": "전쟁" },
  { "id": 37, "name": "서부" },
  { "id": 10402, "name": "음악" },
  { "id": 36, "name": "역사" },
  { "id": 10751, "name": "가족" },
  { "id": 14, "name": "판타지" },
  { "id": 15, "name": "이야기" },
  { "id": 33, "name": "미스터리" },
  { "id": 50, "name": "로맨스" },
  { "id": 11, "name": "공포" },
  { "id": 10769, "name": "외국" }
]


onMounted(async() => {
  store.getMovies();
  console.log('Movies in store:', store.movies); // movies 상태 확인
  store.getMovieDetail(movieId)
  movie.value = store.movieDetail
  store.getMovieReviews(movieId)
  // store.movies에서 해당 movieId에 맞는 영화를 찾음


  // 영화의 러닝타임을 가져옴
  await getMovieRuntime(movie.value.tmdb_Id);
  
  // const movie = store.movies.find((movie)) movie.id == movieId)
  
  await getKeyword(movie.value.tmdb_Id);
  // keywords.value = movieKeywords; // 영화의 러닝타임을 상태에 저장
  
  // movies가 비어있지 않으면 로딩 상태 false로 설정
  const interval = setInterval(() => {
    if (store.movies.length > 0) {
      isLoading.value = false;
      clearInterval(interval);
    }
  }, 100);
  
  
})

const updateMovieData = async () => {
  store.getMovieReviews(movieId)  // 해당 영화의 리뷰 업데이트
  store.getMovies()  // 전체 영화 정보 업데이트
  store.getMovieDetail(movieId)
}

// const getGenres = (genreIds) => {
//   // genreIds 배열을 장르 이름으로 변환
//   const genres = genreIds.map(id => {
//     const genre = genreList.find(g => g.id === id);
//     return genre ? genre.name : null;
//   });

//   // 배열의 장르 이름들을 ' / '로 연결
//   return genres.filter(Boolean).join(' / ');
// }

// 예고편 모달 열기
const openTrailerModal = () => {
  isModalVisible.value = true;
}

// 예고편 모달 닫기
const closeTrailerModal = () => {
  isModalVisible.value = false;
}

</script>

<style scoped>

</style>