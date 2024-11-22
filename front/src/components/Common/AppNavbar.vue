<template>
  <nav>
    <RouterLink :to="{ name: 'ArticleView' }">Articles</RouterLink> |
    <RouterLink v-if="!isLoggedIn" :to="{ name: 'SignUpView' }">SignUpView</RouterLink> |
    <RouterLink v-if="!isLoggedIn" :to="{ name: 'LogInView' }">LogInView</RouterLink> | 
    <RouterLink to="/movies">Movies</RouterLink> |
    <RouterLink to="/review-search">리뷰 검색</RouterLink> |
    <RouterLink to="/recommended">영화 추천</RouterLink>
    <div v-if="isLoggedIn">
      <form @submit.prevent="logOut">
        <input type="submit" value="Logout">
      </form>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterView, RouterLink } from 'vue-router'

const store = useCounterStore()

const logOut = function () {
  store.logOut()
}
const isLoggedIn = computed(() => store.isLogin)
</script>

<style scoped>

</style>