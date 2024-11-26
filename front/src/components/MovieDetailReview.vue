<!-- MovieDetailReview.vue -->
<template>
  <div>
    <hr />

    <div v-if="store.reviews.length === 0">작성된 리뷰가 없습니다.</div>
    <MovieDetailReviewItem
      v-else
      v-for="review in store.reviews"
      :key="review.id"
      :review="review"
      :tmdb_id="tmdb_id"
      @reviewDeleted="onReviewDeleted"
    />

    <h1>리뷰 작성</h1>
    <form @submit.prevent="createReview(movie_pk)">
      

      <!-- 평점 -->
      <div>
        <label for="rate">평점</label>
        <div class="flex gap-2">
          <img
            v-for="i in 10"
            :key="'rate-' + i"
            :src="getStarImage(rate, i)"
            alt="star"
            @click="setRate(i)"
            class="w-8 cursor-pointer"
          />
        </div>
      </div>

      <!-- 공포지수 -->
      <div>
        <label for="fear_score">공포</label>
        <div class="flex gap-2">
          <img
            v-for="i in 10"
            :key="'fear_score-' + i"
            :src="getGhostImage(fear_score, i)"
            alt="star"
            @click="setFearScore(i)"
            class="w-8 cursor-pointer"
          />
        </div>
      </div>

      <!-- 내용 입력 -->
      <div>
        <label for="content">내용</label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>

      <input type="submit" value="제출" />
    </form>
  </div>
</template>

<script setup>
import MovieDetailReviewItem from "@/components/MovieDetailReviewItem.vue";
import { ref, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { useRouter } from "vue-router";

const store = useCounterStore();
const title = ref(null);
const content = ref(null);
const rate = ref(null);
const fear_score = ref(null);
const router = useRouter();

const reviews = computed(() => store.reviews || []);

const emit = defineEmits(["reviewCreated"]);

defineProps({
  movie_pk: String,
});

// 평점 및 공포지수 이미지 결정 함수
const getStarImage = (score, index) => {
  if (index <= score) {
    return '/images/star_full.png'; // 꽉 찬 별
  }
  return '/images/star_empty.png'; // 빈 별
};

const getGhostImage = (score, index) => {
  if (index <= score) {
    return '/images/ghost_full.png'; // 꽉 찬 별
  }
  return '/images/ghost_empty.png'; // 빈 별
};

// 평점 값 설정
const setRate = (value) => {
  rate.value = value;
};

// 공포지수 값 설정
const setFearScore = (value) => {
  fear_score.value = value;
};

// 리뷰 생성
const createReview = async function (movie_pk) {
  await axios({
    method: "post",
    url: `${store.API_URL}/api/v1/${movie_pk}/reviews/`,
    data: {
      rate: rate.value,
      fear_score: fear_score.value,
      content: content.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  });
  // 입력 폼 초기화
  content.value = "";
  rate.value = null;
  fear_score.value = null;

  // 리뷰 목록과 영화 정보 갱신
  await store.getMovieReviews(movie_pk);
  await store.getMovieDetail(movie_pk);
  window.alert("성공");
  emit("reviewChange");
};

// 리뷰 삭제 후 갱신
const onReviewDeleted = async () => {
  await store.getMovieReviews(movie_pk);
  await store.getMovieDetail(movie_pk);
  emit("reviewChange");
};
</script>

<style scoped>
/* 전체 폼 컨테이너 */
form {
  width: 100%; /* 전체 너비 차지 */
  background-color: rgba(20, 20, 20, 0.9);
  border: 2px solid #570000;
  border-radius: 10px;
  padding: 20px;
  color: #f0f0f0;
  margin: 0 auto; /* 가운데 정렬 */
  box-shadow: 0 0 15px rgba(87, 0, 0, 0.5);
}

/* 반응형 미디어 쿼리 추가 */
@media (max-width: 600px) {
  form {
    padding: 15px;
    width: 95%; /* 모바일에서 약간의 여백 */
  }
}

/* 레이블 스타일 */
label {
  color: #ff4040;
  font-weight: bold;
  margin-bottom: 10px;
  display: block; /* 레이블 전체 너비 차지 */
}

/* 텍스트 에리어 */
textarea {
  width: 100%;
  background-color: #2a2a2a;
  color: #ffffff;
  border: 1px solid #570000;
  border-radius: 5px;
  padding: 10px;
  margin-top: 10px;
  min-height: 100px; /* 텍스트 에리어 최소 높이 */
  resize: vertical; /* 수직으로만 리사이즈 가능 */
}

/* 평점, 공포지수 컨테이너 */
.flex {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

/* 제출 버튼 */
input[type="submit"] {
  width: 100%; /* 전체 너비 차지 */
  background-color: #570000;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 15px;
}

input[type="submit"]:hover {
  background-color: #740000;
}

/* 별/유령 이미지 */
.cursor-pointer {
  transition: transform 0.2s ease;
  width: 2rem;
  height: 2rem;
}

.cursor-pointer:hover {
  transform: scale(1.2);
}
</style>
