<!-- components/Common/AppNavbar.vue -->
<template>
  <nav class="bg-black text-white p-4 flex items-center">
    <!-- 로고 이미지 추가 -->
    <RouterLink :to="{ name: 'HomeView' }">
      <img src="@/assets/logo.png" alt="Logo" class="h-8 mr-4"> <!-- 로고 이미지 -->
    </RouterLink>
    
    <!-- 네비게이션 링크들 왼쪽 정렬, 일정한 간격 유지 -->
    <div class="flex space-x-6"> <!-- 왼쪽 링크들 간의 간격 설정 -->
      <RouterLink :to="{ name: 'HomeView' }" class="hover:text-gray-400">Home</RouterLink>
      <RouterLink :to="{ name: 'ArticleView' }" class="hover:text-gray-400">Articles</RouterLink>
      <RouterLink to="/movies" class="hover:text-gray-400">Movies</RouterLink>
      <RouterLink to="/review-search" class="hover:text-gray-400">리뷰 검색</RouterLink>
      <RouterLink to="/recommended" class="hover:text-gray-400">영화 추천</RouterLink>
      <RouterLink to="/random" class="hover:text-gray-400">랜덤</RouterLink>
    </div>

    <!-- 로그인, 회원가입을 오른쪽으로 이동 -->
    <div class="ml-auto flex space-x-4">
      <RouterLink v-if="!isLoggedIn" :to="{ name: 'LogInView' }" class="hover:text-gray-400">로그인</RouterLink>
      <RouterLink v-if="!isLoggedIn" :to="{ name: 'SignUpView' }" class="hover:text-gray-400">회원가입</RouterLink>
    </div>

    <div v-if="isLoggedIn" class="mt-4">
      <form @submit.prevent="logOut">
        <input type="submit" value="Logout" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 cursor-pointer">
      </form>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

const logOut = function () {
  store.logOut()
}
const isLoggedIn = computed(() => store.isLogin)
</script>

<style scoped>
</style>
