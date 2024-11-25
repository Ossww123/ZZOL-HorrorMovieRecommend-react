<!-- MovieDetailReviewItem.vue -->
<template>
    <div>
      <h5>{{ review.id }}</h5>
      <p>Nickname: {{ review.user.nickname }}</p>
      <p>rate: {{ review.rate }}</p>
      <p>fear_score: {{ review.fear_score }}</p>
      <p>content: {{ review.content }}</p>
      <button @click="deleteReview(tmdb_id, review.id)">삭제</button>
      <ReviewCommentsList 
      :review_pk="review.id"
      :movie_pk="tmdb_id"
      />
      <hr>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { useCounterStore } from '@/stores/counter';
  import ReviewCommentsList from './ReviewCommentsList.vue';
  
  
  const store = useCounterStore();

  const emit = defineEmits(['reviewChange'])
  
  defineProps({
    review: Object,
    tmdb_id: String
  })
  
  const deleteReview = async function (tmdb_id, reviewId) {
    axios({
          method: 'delete'  ,
          url: `${store.API_URL}/api/v1/random/${tmdb_id}/reviews/${reviewId}/` , 
          headers: {
            Authorization: `Token ${store.token}`
          }
        })
          console.log("제발 됬다고 말해222222")
          await store.getRandomMovieReviews(tmdb_id)
          emit('reviewDeleted')
          window.alert('성공')
        }
  
  </script>
  