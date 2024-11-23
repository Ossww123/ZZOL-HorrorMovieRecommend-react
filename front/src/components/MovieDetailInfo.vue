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
     <!-- 감독 정보 -->
     <h3>감독</h3>
    <div class="director-section">
      <div v-for="directorId in movie.movie_director" :key="directorId" class="director-card">
        <div v-if="directors[directorId]">
          <img 
            v-if="directors[directorId].profile_path" 
            :src="`https://image.tmdb.org/t/p/w200${directors[directorId].profile_path}`" 
            :alt="directors[directorId].name"
          >
          <div class="director-info">
            <p>{{ directors[directorId].name }}</p>
            <p>{{ directors[directorId].original_name }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 배우 정보 -->
    <h3>출연 배우</h3>
    <div class="actor-section">
      <div v-for="actorId in movie.movie_actor" :key="actorId" class="actor-card">
        <div v-if="actors[actorId]">
        <img
          v-if="actors[actorId].profile_path" 
          :src="`https://image.tmdb.org/t/p/w200${actors[actorId].profile_path}`" 
          :alt="actors[actorId].name"
        >
        <div class="actor-info">
          <p>{{ actors[actorId].name }}</p>
          <p>{{ actors[actorId].original_name }}</p>
        </div>
      </div>
    </div>
  </div>
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
const directors = ref({})
const actors = ref({})

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



const getDirector = async (directorId) => {
    const response = await axios.get(`${store.API_URL}/api/v1/directors/${directorId}/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    directors.value[directorId] = response.data
}

const getActor = async (actorIds) => {
  for (const actorId of actorIds) {
    const response = await axios.get(`${store.API_URL}/api/v1/actors/${actorId}/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    actors.value[actorId] = response.data
  }
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
  
  getDirector(movie.value.movie_director)
  console.log('감독')
  console.log(movie.value.movie_director)
  getActor(movie.value.movie_actor)
  console.log('배우')
  console.log(movie.value.movie_actor)

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
.director-section,
.actor-section {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.director-card,
.actor-card {
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.director-card:hover,
.actor-card:hover {
  transform: translateY(-5px);
}

.director-card img,
.actor-card img {
  width: 100%;
  height: 225px;
  object-fit: cover;
}

.director-info,
.actor-info {
  padding: 10px;
  text-align: center;
}

.director-info p,
.actor-info p {
  margin: 5px 0;
}

/* 이미지가 없는 경우 대체 스타일 */
.director-card:not(:has(img)),
.actor-card:not(:has(img)) {
  background: #333;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>