<template>
  <div>
  <h1>왓챠미디아 사용자 평</h1>
  <p>{{  movie_pk }}</p>
  <div>
    <h1>리뷰 작성</h1>
    <form @submit.prevent="createReview(movie_pk)">
      <!-- 내용 입력 -->
      <div>
          <label for="content">내용 : </label>
          <textarea id="content" v-model.trim="content"></textarea>
        </div>

        <!-- int값 rate 입력 -->
        <div>
          <label for="rate">평점 (1-10): </label>
          <input
            type="number"
            id="rate"
            v-model.number="rate"
            min="1"
            max="10"
            required
          />
        </div>

        <!-- int값 fear_score 입력 -->
        <div>
          <label for="fear_score">공포지수 (1-10): </label>
          <input
            type="number"
            id="fear_score"
            v-model.number="fear_score"
            min="1"
            max="10"
            required
          />
        </div>

        <input type="submit" value="제출">
    </form>
    <hr>
  </div>
   <div v-if="store.reviews.length === 0">
      작성된 리뷰가 없습니다.
    </div>
  <MovieDetailReviewItem
  v-else
  v-for="review in store.reviews"
  :key="`review-${review.id}-${Date.now()}`"
  :review="review"
  :movie_pk="movie_pk"
  @reviewDeleted="onReviewDeleted"
/>
  </div>
</template>

<script setup>
  import MovieDetailReviewItem from '@/components/MovieDetailReviewItem.vue'
  import { ref, computed } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const store = useCounterStore()
  const title = ref(null)
  const content = ref(null)
  const rate = ref(null)
  const fear_score = ref(null)
  const router = useRouter()

  const reviews = computed(() => store.reviews || [])


  const emit = defineEmits(['reviewCreated'])

  defineProps({
    movie_pk: String
  })

  

  const createReview = async function (movie_pk) {
    await axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/${movie_pk}/reviews/`,
      data: {
        rate: rate.value,
        fear_score: fear_score.value,
        content: content.value,
      },
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    // 입력 폼 초기화
    content.value = ''
    rate.value = null
    fear_score.value = null
    
    // 리뷰 목록과 영화 정보 갱신
    await store.getMovieReviews(movie_pk)
    await store.getMovieDetail(movie_pk)
    window.alert('성공')
    emit('reviewChange')
  
}

  const onReviewDeleted = async () => {
    await store.getMovieReviews(movie_pk)
    await store.getMovieDetail(movie_pk)
    emit('reviewChange')
  }
</script>

<style scoped>

</style>