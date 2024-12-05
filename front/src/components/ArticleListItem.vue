<!-- ArticleListItem.vue -->
<template>
  <div class="article-item">
    <div class="article-header">
      <h5>#{{ article.id }}</h5>
      <span class="recommend-count">
        추천 {{ article.recommend_users?.length || 0 }}
      </span>
    </div>

    <div class="article-content-wrapper">
      <p class="article-title">{{ article.title }}</p>
      <p class="article-content">{{ truncateContent(article.content) }}</p>
    </div>

    <div class="article-footer">
      <div class="article-info">
        <span class="author">작성자: {{ article.user.nickname }}</span>
        <span class="date">{{ formatDate(article.created_at) }}</span>
      </div>
      <RouterLink
        :to="{ name: 'DetailView', params: { id: article.id } }"
        class="detail-link"
      >
        상세 보기
      </RouterLink>
    </div>
    <hr />
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";

defineProps({
  article: Object,
});

const truncateContent = (content) => {
  return content.length > 100 ? content.slice(0, 100) + "..." : content;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("ko-KR");
};
</script>

<style scoped>
.article-item {
  background-color: #1a202c;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 카드 그림자 */
  transition: transform 0.3s, box-shadow 0.3s; /* 호버 효과 */
}

.article-item:hover {
  transform: scale(1.03); /* 호버 시 약간 확대 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4); /* 호버 시 그림자 강조 */
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.recommend-count {
  color: #e53e3e;
  font-weight: bold;
}

.article-content-wrapper {
  margin-bottom: 20px;
}

.article-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #e53e3e;
  margin-bottom: 10px;
}

.article-content {
  font-size: 1rem;
  color: #cbd5e0;
  margin-bottom: 10px;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.article-info {
  display: flex;
  gap: 20px;
  color: #a0aec0;
}

.detail-link {
  display: inline-block;
  padding: 8px 16px;
  background-color: #e53e3e;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.detail-link:hover {
  background-color: #c53030;
}

hr {
  border: 1px solid #2d3748;
  margin: 0;
}

@media (max-width: 768px) {
  .article-item {
    padding: 15px;
  }

  .article-title {
    font-size: 1.125rem;
  }

  .article-content {
    font-size: 0.875rem;
  }

  .article-footer {
    flex-direction: column;
    gap: 10px;
  }

  .article-info {
    flex-direction: column;
    gap: 5px;
  }
}
</style>
