<!-- ArticleListItem.vue -->
<template>
  <div>
    <h5>{{ article.id }}</h5>
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
    <!-- 작성자 이름 표시 -->
    <p><strong>작성자:</strong> {{ article.user }}</p>
    <RouterLink 
      :to="{ name: 'DetailView', params: { id: article.id } }"  
    >
      Detail
    </RouterLink>
    <hr>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object  // 부모 컴포넌트에서 article을 props로 받음
})
</script>
