<!-- ArticleList.vue -->
<template>
  <div class="article-list">
    <h3>게시글 목록</h3>
    <div v-if="store.articles.top_articles?.length" class="top-articles">
      <h4>인기 게시글</h4>
      <ArticleListItem
        v-for="article in store.articles.top_articles"
        :key="article.id"
        :article="article"
        class="top-article"
      />
    </div>
    <div
      v-if="store.articles.remaining_articles?.length"
      class="regular-articles"
    >
      <h4>최신 게시글</h4>
      <ArticleListItem
        v-for="article in store.articles.remaining_articles"
        :key="article.id"
        :article="article"
      />
    </div>
  </div>
</template>

<script setup>
import ArticleListItem from "@/components/ArticleListItem.vue";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
</script>

<style scoped>
.article-list {
  padding: 20px;
  background-color: #121212; /* 어두운 배경 */
  color: #fff;
}

h3 {
  font-size: 1.75rem;
  font-weight: bold;
  color: #e53e3e; /* 강렬한 빨간색 */
  margin-bottom: 20px;
  border-bottom: 3px solid #e53e3e; /* 제목 하단 강조 */
  padding-bottom: 5px;
}

h4 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #e53e3e;
}

.top-articles,
.regular-articles {
  display: grid;
  gap: 20px;
  margin-bottom: 40px;
}

@media (max-width: 768px) {
  .article-list {
    padding: 10px;
  }

  h3 {
    font-size: 1.5rem;
  }

  h4 {
    font-size: 1.25rem;
  }

  .top-articles,
  .regular-articles {
    grid-template-columns: 1fr;
  }
}
</style>
