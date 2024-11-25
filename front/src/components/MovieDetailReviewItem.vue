<!-- MovieDetailReviewItem.vue -->
<template>
  <div>
    <h5>{{ review.id }}</h5>
    <p>Nickname: {{ review.user.nickname }}</p>
    <p>rate: {{ review.rate }}</p>
    <p>fear_score: {{ review.fear_score }}</p>
    <p>content: {{ review.content }}</p>
    <button @click="deleteReview(movie_pk, review.id)">삭제</button>
    <ReviewCommentsList
      :key="`comments-${review.id}-${Date.now()}`"
      :review_pk="review.id"
      :movie_pk="movie_pk"
    />
    <hr />
  </div>
</template>

<script setup>
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import ReviewCommentsList from "./ReviewCommentsList.vue";

const store = useCounterStore();
const emit = defineEmits(["reviewDeleted"]);

defineProps({
  review: Object, // 부모 컴포넌트에서 article을 props로 받음
  movie_pk: String,
});

const deleteReview = async function (movie_pk, reviewId) {
  await axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/${movie_pk}/reviews/${reviewId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  });

  console.log("제발 됬다고 말해222222");
  await store.getMovieReviews(movie_pk);
  emit("reviewDeleted");
  window.alert("성공");
};
</script>
