<template>
  <div>
    <h1>왓챠미디아 사용자 평</h1>
    <p>{{ tmdb_id }}</p>
    <div>
      <h1>리뷰 작성</h1>
      <form @submit.prevent="createReview(tmdb_id)">
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

        <input type="submit" value="제출" />
      </form>
      <hr />
    </div>
    <div v-if="store.reviews.length === 0">작성된 리뷰가 없습니다.</div>
    <RandomMovieDetailReviewItem
      v-else
      v-for="review in store.reviews"
      :key="review.id"
      :review="review"
      :tmdb_id="tmdb_id"
      @reviewDeleted="onReviewDeleted"
    />
  </div>
</template>
  
  <script setup>
    import RandomMovieDetailReviewItem from '@/components/RandomMovieDetailReviewItem.vue'
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
  
    const emit = defineEmits(['reviewChange'])
  
    const props = defineProps({
    tmdb_id: String
})
  
    
  
    const createReview = function (tmdb_id) {
        axios({
          method: 'post'  ,
          url: `${store.API_URL}/api/v1/random/${tmdb_id}/reviews/` , 
          data: {
            rate: rate.value,
            fear_score: fear_score.value,
            content: content.value,
          },
          headers: {
            Authorization: `Token ${store.token}`
          }
        })
        .then(async (res) => {
          console.log("제발 됬다고 말해")
          window.alert('성공!')
          content.value = ''
          rate.value = null
          fear_score.value = null
          emit('reviewChange')
        })
        .catch((err) => {
          if (err.response.data.error) {
        alert(err.response.data.error)
      }
        })
      }
      
      const onReviewDeleted = async () => {
        await store.getRandomMovieReviews(props.tmdb_id)
        await store.getRandomMovieDetail(props.tmdb_id)
        emit('reviewChange')
      }
  </script>
  
  <style scoped>
  
  </style>