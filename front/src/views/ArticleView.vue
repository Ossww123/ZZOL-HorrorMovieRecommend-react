<template>
  <div :style="containerStyle" class="content-container">
    <h1>Article Page</h1>
    <RouterLink :to="{ name: 'CreateView' }" class="create-link">Create</RouterLink>
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
import { onMounted, ref, watch, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import { RouterLink } from "vue-router";
import { debounce } from "lodash";

const store = useCounterStore();
const searchKeyword = ref('')
const filteredArticles = ref([])

// Container style
const containerStyle = computed(() => {
  const width = window.innerWidth;
  let containerWidth = 1500;
  
  if (width < 1500) {
    containerWidth = width * 0.67;
  } else if (width < 1200) {
    containerWidth = width * 0.67;
  }

  const sideSpace = Math.max(width * 0.05, 20); // Calculating side space (same as in your previous code)

  return {
    maxWidth: `${containerWidth}px`,
    width: '100%',
    margin: '0 auto',
    padding: `0 ${sideSpace * 1.5}px`, // Adjusting padding for side space
  };
});

const handleSearch = debounce(async () => {
  const results = await store.searchArticles(searchKeyword.value)
  filteredArticles.value = results
}, 300)

onMounted(() => {
  store.getArticles();
  handleSearch()
});
</script>

<style scoped>
/* Your existing styles */
.content-container {
  position: relative;
  width: 100%;
  margin: 0 auto;
  /* Removing old padding here */
}
</style>
