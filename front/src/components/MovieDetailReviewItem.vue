<!-- MovieDetailReviewItem.vue -->
<template>
  <div class="review-container">
    <div class="review-header">
      <div class="user-profile">
        <div class="user-avatar">
          {{ review.user.nickname[0].toUpperCase() }}
        </div>
        <div class="user-info">
          <span class="nickname">{{ review.user.nickname }}</span>
          <span class="timestamp">방금 전</span>
        </div>
      </div>
      <button 
        @click="deleteReview(movie_pk, review.id)" 
        class="delete-button"
      >
        🗑️
      </button>
    </div>

    <div class="review-content">
      <p>{{ review.content }}</p>
    </div>

    <div class="review-ratings">
      <div class="rating-section">
        <span class="rating-label">평점</span>
        <div class="rating-icons">
          <img
            v-for="i in 10"
            :key="'rate-' + i"
            :src="getStarImage(review.rate, i)"
            alt="star"
            class="star-icon"
          />
        </div>
      </div>

      <div class="rating-section">
        <span class="rating-label">공포</span>
        <div class="rating-icons">
          <img
            v-for="i in 10"
            :key="'ghost-' + i"
            :src="getGhostImage(review.rate, i)"
            alt="ghost"
            class="star-icon"
          />
        </div>
      </div>
    </div>
    
    <ReviewCommentsList
      :key="`comments-${review.id}-${Date.now()}`"
      :review_pk="review.id"
      :movie_pk="movie_pk"
    />
  </div>
</template>

<script setup>
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import ReviewCommentsList from "./ReviewCommentsList.vue";

const store = useCounterStore();
const emit = defineEmits(["reviewDeleted"]);

defineProps({
  review: Object,
  movie_pk: String,
});

// 평점에 따른 별 이미지 결정 함수
const getStarImage = (score, index) => {
  if (index <= score) {
    return '/images/star_full.png'; // 꽉 찬 별
  } else if (index - 0.5 === score) {
    return '/images/star_half.png'; // 반 별
  }
  return '/images/star_empty.png'; // 빈 별
};

// 공포지수에 따른 유령 이미지 결정 함수
const getGhostImage = (score, index) => {
  if (index <= score) {
    return '/images/ghost_full.png'; // 꽉 찬 별
  } else if (index - 0.5 === score) {
    return '/images/star_half.png'; // 반 별
  }
  return '/images/ghost_empty.png'; // 빈 별
};

// 리뷰 삭제 함수
const deleteReview = async function (movie_pk, reviewId) {
  await axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/${movie_pk}/reviews/${reviewId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  });

  await store.getMovieReviews(movie_pk);
  emit("reviewDeleted");
  window.alert("리뷰가 삭제되었습니다.");
};
</script>

<style scoped>
.review-container {
  background-color: rgba(25, 25, 25, 0.95);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  color: #e0e0e0;
  border: 1px solid rgba(87, 0, 0, 0.5);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.user-profile {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background-color: #570000;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.nickname {
  font-weight: bold;
}

.timestamp {
  font-size: 0.8em;
  color: #888;
}

.delete-button {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.delete-button:hover {
  opacity: 1;
}

.review-content {
  margin-bottom: 15px;
  line-height: 1.6;
}

.review-ratings {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 15px;
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-label {
  color: #ff4040;
  font-weight: bold;
  min-width: 70px;
}

.rating-icons {
  display: flex;
  gap: 5px;
}

.star-icon {
  width: 1.2rem;
  height: 1.2rem;
  transition: transform 0.2s ease;
}

.star-icon:hover {
  transform: scale(1.2);
}
</style>