<!-- DetailView.vue -->
<template>
  <div
    class="max-w-4xl mx-auto p-4 bg-gray-900 text-white rounded-lg shadow-md"
  >
    <h1 class="text-3xl font-semibold text-red-500 mb-6">게시글 상세</h1>
    <div v-if="article">
      <!-- 게시글 상세 정보 -->
      <div class="bg-gray-800 p-6 rounded-lg mb-6">
        <p class="text-sm text-gray-400">
          게시글 번호: <span class="text-white">{{ article.id }}</span>
        </p>
        <p class="text-lg font-bold text-white mt-2">
          제목: {{ article.title }}
        </p>
        <p class="text-gray-300 mt-2">
          닉네임: <span class="text-red-400">{{ article.user.nickname }}</span>
        </p>
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
          {{ isRecommended ? "추천 취소" : "추천" }} ({{ recommendCount }})
        </button>
      </div>

      <!-- 댓글 섹션 -->
      <ArticleCommentList :article="article" />
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";
import ArticleCommentList from "@/components/ArticleCommentList.vue";

const store = useCounterStore();
const route = useRoute();
const article = ref(null);
const isRecommended = ref(false);
const recommendCount = ref(0);

// 게시글 조회
onMounted(() => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`,
  })
    .then((res) => {
      article.value = res.data;
      checkRecommendStatus();
    })
    .catch((err) => {
      console.log(err);
    });
});

// 추천하기
const Recommend = async function (articleId) {
  try {
    const response = await axios({
      method: "post",
      url: `${store.API_URL}/api/v1/articles/${articleId}/recommends/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    isRecommended.value = !isRecommended.value;
    recommendCount.value = response.data.recommend_count;

    // 추천 상태 변경 후 게시글 정보 업데이트
    const articleResponse = await axios({
      method: "get",
      url: `${store.API_URL}/api/v1/articles/${articleId}/`,
    });
    article.value = articleResponse.data;
  } catch (err) {
    console.log(err);
  }
};

// 추천 상태 확인
const checkRecommendStatus = () => {
  if (article.value && article.value.recommend_users) {
    isRecommended.value = article.value.recommend_users.includes(store.user_id);
    recommendCount.value = article.value.recommend_users.length;
  }
};
</script>

<style scoped>
.detail-view {
  padding: 20px;
  background-color: #121212; /* 어두운 배경 */
  color: white;
}

.detail-title {
  font-size: 2rem;
  font-weight: bold;
  color: #e53e3e; /* 공포 영화 느낌의 빨간색 */
  margin-bottom: 20px;
  text-align: center;
}

.article-detail-card {
  background-color: #1a202c;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 30px;
}

.article-header {
  margin-bottom: 20px;
}

.article-id {
  font-size: 1rem;
  color: #cbd5e0; /* 밝은 회색 */
}

.article-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #f56565; /* 빨간색 */
  margin-top: 10px;
}

.article-meta {
  font-size: 0.875rem;
  color: #e2e8f0;
  margin-bottom: 20px;
}

.author-name {
  color: #f56565; /* 닉네임 강조 */
}

.article-content {
  font-size: 1.125rem;
  color: #e2e8f0;
  line-height: 1.6;
}

.recommend-section {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.recommend-button {
  padding: 10px 20px;
  background-color: #f56565;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s, transform 0.3s;
}

.recommend-button:hover {
  background-color: #c53030;
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .detail-title {
    font-size: 1.75rem;
  }

  .article-title {
    font-size: 1.25rem;
  }

  .article-content {
    font-size: 1rem;
  }
}
</style>
