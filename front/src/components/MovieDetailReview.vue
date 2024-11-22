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
  </div>
  <MovieDetailReviewItem
      v-for="review in store.reviews"
      :key="review.id"
      :review="review"
      :movie_pk="movie_pk"
    />
    
  </div>
</template>

<script setup>
  import MovieDetailReviewItem from '@/components/MovieDetailReviewItem.vue'
  import { ref } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const store = useCounterStore()
  const title = ref(null)
  const content = ref(null)
  const rate = ref(null)
  const fear_score = ref(null)
  const router = useRouter()

  defineProps({
    movie_pk: String
  })

  const createReview = function (movie_pk) {
      axios({
        method: 'post'  ,
        url: `${store.API_URL}/api/v1/${movie_pk}/reviews/` , 
        data: {
          rate: rate.value,
          fear_score: fear_score.value,
          content: content.value,
        },
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      .then((res) => {
        console.log("제발 됬다고 말해")
      })
      .catch((err) => {
        console.log("응 안돼 돌아가")
        console.log(err)
      })
    }

</script>

<style scoped>

</style>