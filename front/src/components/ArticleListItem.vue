<template>
  <div class="article-item">
    <h5>{{ article.id }}</h5>
    <p class="article-title">{{ article.title }}</p>
    <p class="article-content">{{ article.content }}</p>
    <p><strong>작성자:</strong> {{ article.user }}</p>
    <RouterLink
      :to="{ name: 'DetailView', params: { id: article.id } }"
      class="detail-link"
    >
      Detail
    </RouterLink>
    <hr />
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";

defineProps({
  article: Object,
});
</script>

<style scoped>
.article-item {
  background-color: #1a202c;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  color: white;
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
  margin-top: 20px;
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
}
</style>
