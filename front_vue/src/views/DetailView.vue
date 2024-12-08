<template>
  <div class="article-detail-container">
    <!-- Article Header -->
    <header class="article-header">
      <h1 class="article-title">게시글 상세</h1>
    </header>

    <!-- Article Content -->
    <div v-if="article" class="article-content-wrapper">
      <section class="article-metadata">
        <div class="metadata-grid">
          <div class="metadata-item">
            <span class="metadata-label">제목:</span>
            <span class="metadata-value title">{{ article.title }}</span>
          </div>
          <div class="metadata-item">
            <span class="metadata-label">작성자:</span>
            <span class="metadata-value author">{{
              article.user.nickname
            }}</span>
          </div>
          <div class="metadata-item metadata-dates">
            <span class="metadata-label date-label">작성일:</span>
            <span class="metadata-value date">{{
              formatDate(article.created_at)
            }}</span>
          </div>
          <div class="metadata-item metadata-dates">
            <span class="metadata-label date-label">수정일:</span>
            <span class="metadata-value date">{{
              formatDate(article.updated_at)
            }}</span>
          </div>
        </div>
      </section>

      <!-- Article Body -->
      <article class="article-body">
        <p class="article-text">{{ article.content }}</p>
      </article>

      <!-- Recommendation Section -->
      <section class="recommendation-section">
        <button @click="Recommend(article.id)" class="recommend-button">
          {{ isRecommended ? "추천" : "추천" }} ({{ recommendCount }})
        </button>
      </section>

      <!-- Comments Section -->
      <section class="comments-section">
        <ArticleCommentList :article="article" />
      </section>
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

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  if (!dateString) return "";
  return dateString.split("T")[0];
};

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

    // 게시글 정보 업데이트
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
.article-detail-container {
  @apply max-w-3xl mx-auto p-6 bg-gray-800 text-white rounded-lg shadow-lg;
}

.article-header {
  @apply mb-8;
}

.article-title {
  @apply text-4xl font-semibold text-red-500;
}

.article-metadata {
  @apply bg-gray-700 p-6 rounded-lg mb-8;
}

.metadata-grid {
  @apply grid grid-cols-2 gap-4;
}

.metadata-item {
  @apply flex items-center;
}

.metadata-label {
  @apply font-bold mr-2 text-sm text-gray-300;
}

.metadata-label.date-label {
  @apply text-xs text-gray-400;
}

.metadata-value {
  @apply text-sm;
}

.metadata-value.title {
  @apply text-xl font-bold text-white;
}

.metadata-value.author {
  @apply text-red-400;
}

.metadata-value.date {
  @apply text-xs text-gray-400;
}

.article-body {
  @apply mb-8;
}

.article-text {
  @apply text-gray-300 leading-relaxed text-base;
}

.recommendation-section {
  @apply flex justify-center mb-8;
}

.recommend-button {
  @apply bg-red-500 hover:bg-red-700 text-white py-3 px-6 
         rounded-lg focus:outline-none 
         transform transition-all duration-300 
         flex items-center gap-2;
}

@media (max-width: 768px) {
  .metadata-grid {
    @apply grid-cols-1;
  }

  .article-title {
    @apply text-3xl;
  }
}
</style>
