<!-- src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <div class="form-container">
      <!-- 바깥쪽 반투명 컨테이너 추가 -->
      <div class="outer-box">
        <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-sm">
          <h1 class="text-3xl font-bold text-center mb-6">Log In</h1>
          <form @submit.prevent="logIn">
            <div class="mb-4">
              <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
              <input type="text" id="username" v-model.trim="username" class="w-full p-2 mt-2 border border-gray-300 rounded-lg" placeholder="Enter your username">
            </div>

            <div class="mb-6">
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input type="password" id="password" v-model.trim="password" class="w-full p-2 mt-2 border border-gray-300 rounded-lg" placeholder="Enter your password">
            </div>

            <div class="flex justify-center">
              <input type="submit" value="Log In" class="w-full p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 cursor-pointer">
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// script 부분은 동일
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 64px);
  width: 100%;
  background-image: url('/images/image.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.form-container {
  min-height: inherit;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

/* 바깥쪽 반투명 박스 스타일 */
.outer-box {
  background-color: rgba(255, 255, 255, 0.15); /* 반투명 흰색 배경 */
  backdrop-filter: blur(8px); /* 블러 효과 추가 */
  border-radius: 20px; /* 둥근 모서리 */
  padding: 2rem; /* 내부 여백 */
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); /* 그림자 효과 */
  border: 1px solid rgba(255, 255, 255, 0.18); /* 미세한 테두리 */
}

/* 내부 폼 컨테이너의 그림자 조정 */
.bg-white {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>