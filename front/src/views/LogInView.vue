<!-- src/views/LogInView.vue -->
<template>
  <div class="container">
    <div class="login-form">
      <h1>Log In</h1>
      <form @submit.prevent="logIn">
        <!-- Username -->
        <label for="username">Username: </label>
        <input type="text" id="username" v-model.trim="username" />
        
        <!-- Password -->
        <label for="password">Password: </label>
        <input type="password" id="password" v-model.trim="password" />
        
        <!-- Submit Button -->
        <input type="submit" value="Log In" :disabled="isSubmitting" />
        
        <!-- 로딩 스피너 -->
        <div v-if="isSubmitting" class="spinner"></div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const password = ref(null)
const isSubmitting = ref(false)


const store = useCounterStore()

const logIn = async () => {
  isSubmitting.value = true
  const payload = {
    username: username.value,
    password: password.value
  }
  
  try {
    await store.logIn(payload)
    // 로그인 성공 후 처리 (예: 성공 메시지, 리디렉션 등)
  } catch (error) {
    // 에러 처리 (예: 로그인 실패 메시지 등)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
/* 오류 메시지 스타일 */
.error {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

/* 전체 화면을 채운 div */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: black;
}

/* 로그인 폼 스타일 */
.login-form {
  background-color: white;
  border: 2px solid #ccc;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
}

/* 폼 요소들에 대한 스타일 */
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

h1 {
  color: black;
  text-align: center;
}

label {
  font-size: 14px;
  margin-bottom: 4px;
  color: black;
}

input {
  padding: 10px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  color: black;
}

input[type="submit"] {
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  border-radius: 6px;
  padding: 10px;
}

input[type="submit"]:hover {
  background-color: #45a049;
}

input[type="submit"]:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 로딩 스피너 스타일 */
.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 10px auto;
}

/* 스피너 회전 애니메이션 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
