<template>
  <div class="app-container">
    <AppNavbar />
    <div :class="['router-container', routeName === 'SignUpView' || routeName === 'LogInView' ? 'centered' : '']">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import AppNavbar from '@/components/Common/AppNavbar.vue'

// 현재 라우트의 이름을 가져옵니다.
const route = useRoute()
const routeName = route.name // 현재 경로 이름
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
  background-color: black; /* 배경색을 지정 */
}

body {
  color: white; /* 텍스트를 흰색으로 설정 */
}

/* AppNavbar 높이를 고정 */
AppNavbar {
  flex-shrink: 0; /* AppNavbar의 크기를 고정 */
}

/* .router-container에 조건부 스타일 적용 */
.router-container {
  flex-grow: 1;
  width: 100%; /* 화면 크기 꽉 차도록 */
}

/* SignUpView와 LoginView에만 적용되는 스타일 */
.router-container.centered {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: black;
}
</style>
