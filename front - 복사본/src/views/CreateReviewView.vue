<!--CreateReviewView.vue-->

<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="createReview">
      <div>
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title">
      </div>
      <div>
        <label for="content">내용 : </label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { useRouter } from 'vue-router'

const title = ref(null)
const content = ref(null)
const store = useCounterStore()
const router = useRouter()

const createReview = function (movie_pk) {
    axios({
      method: 'post'  ,
      url: `${API_URL}/api/v1/${movie_pk}/reviews/` , 
      data: {
        rate: rate.value,
        fear_index: fear_index.value,
        content: content.value,
      },
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      console.log("제발 됬다고 말해")
      router.push({ name: 'MovieDetailView'})
    })
    .catch((err) => {
      console.log("응 안돼 돌아가")
      console.log(err)
    })
  }

</script>

<style>

</style>
