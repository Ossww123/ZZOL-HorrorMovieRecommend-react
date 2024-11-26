<template>
  <div class="max-w-4xl mx-auto p-4 bg-gray-900 text-white rounded-lg shadow-md">
    <h1 class="text-3xl font-semibold text-red-500 mb-6">게시글 상세</h1>
    <div v-if="article">
      <!-- 게시글 상세 정보 -->
      <div class="bg-gray-800 p-6 rounded-lg mb-6">
        <p class="text-sm text-gray-400">게시글 번호: <span class="text-white">{{ article.id }}</span></p>
        <p class="text-lg font-bold text-white mt-2">제목: {{ article.title }}</p>
        <p class="text-gray-300 mt-2">닉네임: <span class="text-red-400">{{ article.user.nickname }}</span></p>
        <p class="text-gray-300 mt-2">작성일: {{ article.created_at }}</p>
        <p class="text-gray-300 mt-2">수정일: {{ article.updated_at }}</p>
        <p class="text-gray-300 mt-4">{{ article.content }}</p>
      </div>

      <!-- 추천 버튼 -->
      <div class="flex items-center gap-4 mb-6">
        <button 
          @click="Recommend(article.id)" 
          class="bg-red-500 hover:bg-red-700 text-white py-2 px-4 rounded-lg focus:outline-none"
        >
          {{ isRecommended ? '추천 취소' : '추천' }} ({{ recommendCount }})
        </button>
      </div>

      <!-- 댓글 섹션 -->
      <ArticleCommentList :article="article" />
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

// 게시글 조회
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`
  })
    .then((res) => {
      article.value = res.data
      console.log(isRecommended.value)
      checkRecommendStatus()
    })
    .catch((err) => {
      console.log(err)
    })
})

// 추천하기
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
    console.log(isRecommended.value)
    recommendCount.value = response.data.recommend_count

    // 추천 상태 변경 후 게시글 정보 업데이트
    const articleResponse = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/articles/${articleId}/`
    })
    article.value = articleResponse.data
    console.log(article.value)
  } catch (err) {
    console.log(err)
  }
}

// 추천 상태 확인
const checkRecommendStatus = () => {
  if (article.value && article.value.recommend_users) {
    isRecommended.value = article.value.recommend_users.includes(store.user_id)
    recommendCount.value = article.value.recommend_users.length
  }
}
</script>

<style scoped>
/* 게시글 페이지 스타일링 */
.bg-gray-900 {
  background-color: #1a202c; /* 어두운 배경 */
}

.text-white {
  color: #ffffff; /* 텍스트 색상 */
}

.text-red-500 {
  color: #f56565; /* 빨간색 */
}

.bg-gray-800 {
  background-color: #2d3748; /* 회색 배경 */
}

.bg-red-500 {
  background-color: #f56565; /* 빨간색 배경 */
}

.bg-red-700 {
  background-color: #c53030; /* 어두운 빨간색 */
}

.hover\:bg-red-700:hover {
  background-color: #c53030; /* hover 효과 */
}

.text-gray-400 {
  color: #cbd5e0; /* 밝은 회색 */
}

.text-gray-300 {
  color: #e2e8f0; /* 더 밝은 회색 */
}

.text-lg {
  font-size: 1.125rem; /* 큰 텍스트 */
}

.text-sm {
  font-size: 0.875rem; /* 작은 텍스트 */
}

.text-center {
  text-align: center; /* 중앙 정렬 */
}

.font-semibold {
  font-weight: 600; /* 중간 두께의 글꼴 */
}

.rounded-lg {
  border-radius: 0.5rem; /* 둥근 모서리 */
}

.shadow-md {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 */
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.mb-6 {
  margin-bottom: 1.5rem;
}

.mt-4 {
  margin-top: 1rem;
}

.mt-2 {
  margin-top: 0.5rem;
}

.gap-4 {
  gap: 1rem;
}

.gap-6 {
  gap: 1.5rem;
}

.max-w-4xl {
  max-width: 56rem; /* 최대 너비 */
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.p-4 {
  padding: 1rem; /* 패딩 */
}

.text-center {
  text-align: center;
}

.focus\:outline-none:focus {
  outline: none;
}
</style>
