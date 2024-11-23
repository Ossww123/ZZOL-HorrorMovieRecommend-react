<template>
  <div class="article-list">
    <h3>Article List</h3>
    <ArticleListItem
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
    />
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
