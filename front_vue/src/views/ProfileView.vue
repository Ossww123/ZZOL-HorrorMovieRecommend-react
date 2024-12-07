<template>
  <div class="profile-container">
    <div class="profile-header">
      <!-- 프로필 이미지 -->
      <div class="profile-image-container">
        <img
          :src="userProfileImage"
          alt="Profile Image"
          class="w-32 h-32 rounded-full border-2 border-white"
        />
      </div>

      <!-- 사용자 정보 -->
      <div class="profile-info">
        <p class="text-lg font-semibold">닉네임: {{ nickname }}</p>
        <p class="text-lg font-semibold">이메일: {{ email }}</p>
      </div>
    </div>

    <!-- 좋아요한 영화 목록 -->
    <div v-if="likedMovies.length" class="liked-movies">
      <h2 class="text-xl font-semibold text-center mb-4">좋아요한 영화 목록</h2>
      <ul class="movie-list">
        <li
          v-for="movie in likedMovies"
          :key="movie.id"
          class="movie-card mb-4"
          @click="goDetail(movie)"
        >
          <img
            :src="'https://image.tmdb.org/t/p/w500' + movie.image"
            alt="Movie Image"
            class="w-24 h-32 object-cover rounded-md mb-2"
          />
          <p class="text-center">{{ movie.title }}</p>
        </li>
      </ul>
    </div>

    <div v-else class="text-center text-gray-400">
      좋아요한 영화가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter"; // store 가져오기
import defaultProfileImage from "@/assets/default-profile.png";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter()

// store에서 필요한 데이터 가져오기
const store = useCounterStore();

// 좋아요한 영화 목록을 저장할 상태 변수
const likedMovies = ref([]);

// 컴포넌트가 마운트되면 fetchUserProfile 호출하여 정보 불러오기
onMounted(() => {
  store.fetchUserProfile();
  fetchLikedMovies();
});

// 프로필 이미지, 닉네임, 이메일을 computed로 반환
const userProfileImage = computed(
  () => store.profileImage || defaultProfileImage
);
const nickname = computed(() => store.nickname || "알 수 없음");
const email = computed(() => store.email || "이메일 없음");

// 좋아요한 영화 목록을 가져오는 함수
const fetchLikedMovies = async () => {
  try {
    const response = await axios.get(
      `${store.API_URL}/api/v1/user/liked-movies/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    likedMovies.value = response.data; // 받아온 영화 목록을 상태에 저장
    console.log(likedMovies.value)
  } catch (error) {
    console.error("좋아요한 영화 목록 가져오기 실패", error);
  }
};


const goDetail = (movie) => {
  router.push(`/random/${movie.tmdb_id}`);
};
</script>

<style scoped>
.profile-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #1f2937; /* 배경색 */
  border-radius: 8px;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-image-container {
  display: flex;
  justify-content: center;
}

.profile-image-container img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff;
}

.profile-info {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.profile-info p {
  margin: 8px 0;
  font-size: 16px;
}

.liked-movies {
  margin-top: 20px;
}

.liked-movies h2 {
  font-size: 20px;
  font-weight: 600;
  text-align: center;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: space-between;
}

.movie-item {
  width: calc(20% - 12px); /* 한 행에 5개씩 배치 (간격을 고려하여 20%로 설정) */
  text-align: center;
}

.movie-item img {
  max-width: 100%;
  height: auto;
  object-fit: cover;
}

.movie-card img {
  width: 100%;  /* 이미지 너비를 카드에 맞춤 */
  height: 150px;  /* 이미지 높이 고정 */
  object-fit: cover;  /* 이미지 비율 유지 */
}

.movie-card {
  width: 100px;  /* 카드 너비 축소 */
  margin: 0 auto;  /* 중앙 정렬 */
  border-radius: 8px;  /* 모서리 둥글기 감소 */
  overflow: hidden;
  background-color: #2d3748;
  color: rgb(255, 255, 255);
  display: flex;
  flex-direction: column;
  align-items: center;  /* 내용 중앙 정렬 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
  cursor: pointer;  /* 클릭 가능함을 표시 */
}

.movie-card p {
  padding: 8px;
  font-size: 0.875rem;  /* 글자 크기 축소 */
  text-align: center;
  word-break: break-word;  /* 긴 제목 처리 */
  max-width: 100%;  /* 텍스트 너비 제한 */
}

.movie-card:hover {
  transform: translateY(-5px); /* 호버 시 살짝 위로 떠오르는 효과 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5); /* 강조된 그림자 */
}


@media (max-width: 768px) {
  .movie-item {
    width: calc(33.33% - 12px); /* 작은 화면에서는 한 행에 3개 */
  }
}

@media (max-width: 480px) {
  .movie-item {
    width: calc(50% - 12px); /* 모바일 화면에서는 한 행에 2개 */
  }
}
</style>
