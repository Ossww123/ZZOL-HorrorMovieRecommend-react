<template>
  <div>
    <h1>Article Page</h1>
    <RouterLink :to="{ name: 'CreateView' }" class="create-link"
      >Create</RouterLink
    >
    <div class="search-box">
      <input 
        type="text" 
        v-model="searchKeyword"
        @input="handleSearch"
        placeholder="검색어를 입력하세요"
      >
    </div>
    <ArticleList :articles="filteredArticles" />
  </div>
</template>

<script setup>
import ArticleList from "@/components/ArticleList.vue";
import { onMounted, ref, watch } from "vue";
import { useCounterStore } from "@/stores/counter";
import { RouterLink } from "vue-router";
import { debounce } from "lodash";

const store = useCounterStore();
const searchKeyword = ref('')
const filteredArticles = ref([])

const handleSearch = debounce(async () => {
  const results = await store.searchArticles(searchKeyword.value)
  filteredArticles.value = results
}, 300)


onMounted(() => {
  // mount 되기전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles();
  handleSearch()
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

.search-box {
  margin: 20px 0;
}

.search-box input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
