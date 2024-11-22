<!--SignUpView.vue-->
<template>
  <div class="container">
    <div class="signup-form">
      <h1>Sign Up Page</h1>
      <form @submit.prevent="signUp">
        <!-- Username -->
        <label for="username">username : </label>
        <input type="text" id="username" v-model.trim="username">
        <p v-if="errors.username" class="error">{{ errors.username }}</p>

        <!-- Email -->
        <label for="email">email : </label>
        <input type="text" id="email" v-model.trim="email">
        <p v-if="errors.email" class="error">{{ errors.email }}</p>

        <!-- Password -->
        <label for="password1">password : </label>
        <input type="password" id="password1" v-model.trim="password1">
        <p v-if="errors.password1" class="error">{{ errors.password1 }}</p>

        <!-- Password confirmation -->
        <label for="password2">password confirmation : </label>
        <input type="password" id="password2" v-model.trim="password2">
        <p v-if="errors.password2" class="error">{{ errors.password2 }}</p>

        <!-- Nickname -->
        <label for="nickname">nickname : </label>
        <input type="text" id="nickname" v-model.trim="nickname">
        <p v-if="errors.nickname" class="error">{{ errors.nickname }}</p>

        <!-- Submit Button -->
        <input type="submit" value="SignUp" :disabled="isSubmitting">
        
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
const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const nickname = ref(null)

const errors = ref({
  username: null,
  email: null,
  password1: null,
  password2: null,
  nickname: null,
})

const isSubmitting = ref(false)

const store = useCounterStore()

// 이메일 형식 확인
const isValidEmail = (email) => {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailPattern.test(email);
}

// 비밀번호 일치 확인
const passwordsMatch = (password1, password2) => {
  return password1 === password2;
}

// 폼 검증 함수
const validateForm = () => {
  let valid = true;
  
  // 오류 초기화
  errors.value = {
    username: null,
    email: null,
    password1: null,
    password2: null,
    nickname: null,
  }

  // username 검증
  if (!username.value) {
    errors.value.username = 'username을 입력하세요.';
    valid = false;
  }

  // email 검증
  if (!email.value) {
    errors.value.email = 'email을 입력하세요.';
    valid = false;
  } else if (!isValidEmail(email.value)) {
    errors.value.email = '잘못된 이메일 형식입니다.';
    valid = false;
  }

  // password1 검증
  if (!password1.value) {
    errors.value.password1 = 'password를 입력하세요.';
    valid = false;
  }

  // password2 검증
  if (!password2.value) {
    errors.value.password2 = 'Password confirmation을 입력하세요.';
    valid = false;
  } else if (!passwordsMatch(password1.value, password2.value)) {
    errors.value.password2 = '비밀번호가 일치하지 않습니다.';
    valid = false;
  }

  // nickname 검증
  if (!nickname.value) {
    errors.value.nickname = 'Nickname을 입력하세요.';
    valid = false;
  }

  return valid;
}

// 회원가입 함수
const signUp = async () => {
  if (!validateForm()) {
    return; // 검증 실패 시 회원가입을 진행하지 않음
  }
  
  isSubmitting.value = true;
  
  const payload = {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
  }
  
  try {
    await store.signUp(payload)
    // 회원가입 성공 후 처리 (예: 성공 메시지, 리디렉션 등)
  } catch (error) {
    // 에러 처리 (예: 서버 오류 메시지 등)
  } finally {
    isSubmitting.value = false;
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

/* 회원가입 폼 스타일 */
.signup-form {
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
