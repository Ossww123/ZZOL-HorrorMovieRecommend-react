<!-- src/App.vue -->
<template>
  <div class="app-container">
    <AppNavbar />
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import AppNavbar from '@/components/Common/AppNavbar.vue'
</script>

<style>
/* 전역 스타일을 위해 scoped 제거 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>