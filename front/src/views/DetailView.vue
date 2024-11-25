<template>
  <div>
    <h1>Detail</h1>
    <div v-if="article">
      <p>게시글 번호 : {{ article.id }}</p>
      <p>제목 : {{ article.title }}</p>
      <p>내용 : {{ article.content }}</p>
      <p>작성일 : {{ article.created_at }}</p>
      <p>수정일 : {{ article.updated_at }}</p>
      <button @click="Recommend(article.id)">
      {{ isRecommended ? '추천' : '추천' }}
      ({{ recommendCount }})
      </button>
      <ArticleCommentList
      :article="article"
      />
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import ArticleCommentList from '@/components/ArticleCommentList.vue'

const store = useCounterStore()
const route = useRoute()
const article = ref(null)
const isRecommended = ref(false)
const recommendCount = ref(0)

// DetailView가 마운트되기전에 DRF로 단일 게시글 조회를 요청 후 응답데이터를 저장
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`
  })
    .then((res) => {
      // console.log(res.data)
      article.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
})


const Recommend = async function(articleId) {
  try {
    const response = await axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/articles/${articleId}/recommends/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    isRecommended.value = !isRecommended.value
    recommendCount.value = response.data.recommend_count
    
    // 추천 상태 변경 후 게시글 정보 업데이트
    const articleResponse = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/articles/${articleId}/`
    })
    article.value = articleResponse.data
  } catch (err) {
    console.log(err)
  }
}



// 현재 사용자의 추천 상태 확인
const checkRecommendStatus = () => {
  if (article.value && article.value.recommend_users) {
    isRecommended.value = article.value.recommend_users.includes(store.user_id)
    recommendCount.value = article.value.recommend_users.length
  }
}


onMounted(async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/articles/${route.params.id}/`
    })
    article.value = response.data
    checkRecommendStatus()
  } catch (err) {
    console.log(err)
  }
})
</script>

<style>

</style>
