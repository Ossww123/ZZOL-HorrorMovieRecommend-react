<template>
  <div>
    <h1>Article Page</h1>
    <RouterLink :to="{ name: 'CreateView' }" class="create-link"
      >Create</RouterLink
    >
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from "@/components/ArticleList.vue";
import { onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { RouterLink } from "vue-router";

const store = useCounterStore();

onMounted(() => {
  // mount 되기전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles();
});
</script>

<style scoped>
h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #e53e3e; /* 빨간색 */
  margin-bottom: 20px;
}

.create-link {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #e53e3e;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.create-link:hover {
  background-color: #c53030;
}
</style>
