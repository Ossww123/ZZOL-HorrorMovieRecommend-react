<template>
  <div class="article-list">
    <h3>게시글 목록</h3>
    <!-- 인기 게시글 (추천순 상위 5개) -->
    <div v-if="store.articles.top_articles?.length" class="top-articles">
      <h4>인기 게시글</h4>
      <ArticleListItem
        v-for="article in store.articles.top_articles"
        :key="article.id"
        :article="article"
        class="top-article"
      />
    </div>
    <!-- 일반 게시글 (최신순) -->
    <div v-if="store.articles.remaining_articles?.length" class="regular-articles">
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
import ArticleListItem from "@/components/ArticleListItem.vue"
import { useCounterStore } from "@/stores/counter"

const store = useCounterStore()


</script>

<style scoped>
.article-list {
  padding: 20px;
}

h3 {
  font-size: 1.75rem;
  font-weight: bold;
  color: #e53e3e;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .article-list {
    padding: 10px;
  }
}
</style>
