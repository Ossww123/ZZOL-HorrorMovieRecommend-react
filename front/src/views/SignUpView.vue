<!--SignUpView.vue-->
<template>
  <div class="w-full max-w-md p-6">
    <div class="bg-white rounded-xl shadow-lg p-8">
      <h1 class="text-2xl font-bold text-black text-center mb-6">
        Sign Up Page
      </h1>

      <form @submit.prevent="signUp" class="flex flex-col gap-4">
        <!-- Username -->
        <div class="flex flex-col">
          <label for="username" class="text-sm text-black mb-1"
            >username :
          </label>
          <input
            type="text"
            id="username"
            v-model.trim="username"
            class="p-2 border border-gray-300 rounded-md text-black"
          />
          <p v-if="errors.username" class="text-red-500 text-xs mt-1">
            {{ errors.username }}
          </p>
        </div>

        <!-- Email -->
        <div class="flex flex-col">
          <label for="email" class="text-sm text-black mb-1">email : </label>
          <input
            type="text"
            id="email"
            v-model.trim="email"
            class="p-2 border border-gray-300 rounded-md text-black"
          />
          <p v-if="errors.email" class="text-red-500 text-xs mt-1">
            {{ errors.email }}
          </p>
        </div>

        <!-- Password -->
        <div class="flex flex-col">
          <label for="password1" class="text-sm text-black mb-1"
            >password :
          </label>
          <input
            type="password"
            id="password1"
            v-model.trim="password1"
            class="p-2 border border-gray-300 rounded-md text-black"
          />
          <p v-if="errors.password1" class="text-red-500 text-xs mt-1">
            {{ errors.password1 }}
          </p>
        </div>

        <!-- Password confirmation -->
        <div class="flex flex-col">
          <label for="password2" class="text-sm text-black mb-1"
            >password confirmation :
          </label>
          <input
            type="password"
            id="password2"
            v-model.trim="password2"
            class="p-2 border border-gray-300 rounded-md text-black"
          />
          <p v-if="errors.password2" class="text-red-500 text-xs mt-1">
            {{ errors.password2 }}
          </p>
        </div>

        <!-- Nickname -->
        <div class="flex flex-col">
          <label for="nickname" class="text-sm text-black mb-1"
            >nickname :
          </label>
          <input
            type="text"
            id="nickname"
            v-model.trim="nickname"
            class="p-2 border border-gray-300 rounded-md text-black"
          />
          <p v-if="errors.nickname" class="text-red-500 text-xs mt-1">
            {{ errors.nickname }}
          </p>
        </div>

        <!-- Profile Image -->
        <div class="flex flex-col">
          <label for="profileimage" class="text-sm text-black mb-1"
            >Profile Image :</label
          >
          <input
            type="file"
            id="profileimage"
            @change="handleImageUpload"
            class="p-2 border border-gray-300 rounded-md text-black"
          />
          <p v-if="errors.profileimage" class="text-red-500 text-xs mt-1">
            {{ errors.profileimage }}
          </p>
        </div>

        <!-- Submit Button -->
        <input
          type="submit"
          value="SignUp"
          :disabled="isSubmitting"
          class="bg-green-500 text-white py-2 px-4 rounded-md cursor-pointer hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed mt-4"
        />

        <!-- 로딩 스피너 -->
        <div v-if="isSubmitting" class="flex justify-center">
          <div
            class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"
          ></div>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup>
import axios from "axios"; // axios import 추가
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

const username = ref(null);
const email = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const nickname = ref(null);
const profileimage = ref(null); // 프로필 이미지 상태 변수 추가
const router = useRouter()

const errors = ref({
  username: null,
  email: null,
  password1: null,
  password2: null,
  nickname: null,
});

const isSubmitting = ref(false);

const store = useCounterStore();

// 이메일 형식 확인
const isValidEmail = (email) => {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailPattern.test(email);
};

// 비밀번호 일치 확인
const passwordsMatch = (password1, password2) => {
  return password1 === password2;
};

const handleImageUpload = (event) => {
  profileimage.value = event.target.files[0]; // 업로드된 첫 번째 파일을 profileimage에 저장
};

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
  };

  // username 검증
  if (!username.value) {
    errors.value.username = "username을 입력하세요.";
    valid = false;
  }

  // email 검증
  if (!email.value) {
    errors.value.email = "email을 입력하세요.";
    valid = false;
  } else if (!isValidEmail(email.value)) {
    errors.value.email = "잘못된 이메일 형식입니다.";
    valid = false;
  }

  // password1 검증
  if (!password1.value) {
    errors.value.password1 = "password를 입력하세요.";
    valid = false;
  }

  // password2 검증
  if (!password2.value) {
    errors.value.password2 = "Password confirmation을 입력하세요.";
    valid = false;
  } else if (!passwordsMatch(password1.value, password2.value)) {
    errors.value.password2 = "비밀번호가 일치하지 않습니다.";
    valid = false;
  }

  // nickname 검증
  if (!nickname.value) {
    errors.value.nickname = "Nickname을 입력하세요.";
    valid = false;
  }

  // if (!profileimage.value) {
  //   errors.value.profileimage = "프로필 이미지를 선택하세요.";
  //   valid = false;
  // }

  return valid;
};

// 회원가입 함수
const signUp = async () => {
  if (!validateForm()) {
    return; // 검증 실패 시 회원가입을 진행하지 않음
  }

  isSubmitting.value = true;

  // FormData 생성
  const formData = new FormData();
  formData.append("username", username.value);
  formData.append("email", email.value);
  formData.append("password1", password1.value);
  formData.append("password2", password2.value);
  formData.append("nickname", nickname.value);
  if (profileimage.value) {
    formData.append("profileimage", profileimage.value); // 프로필 이미지가 있을 경우 추가
  }

  try {
    // 요청 보내기
    await axios.post("http://127.0.0.1:8000/accounts/signup/", formData, {
      headers: {
        Accept: "application/json",
        // 'Content-Type'은 FormData를 사용할 때 자동으로 설정되므로 제거
      },
    });
    const loginData = {
      username: username.value,
      password: password1.value
    };
    
    const loginResponse = await axios.post("http://127.0.0.1:8000/accounts/login/", loginData);
    
    // 토큰 저장 및 상태 업데이트
    store.token = loginResponse.data.key;
    await store.fetchUserProfile();
    
    // 홈으로 이동
    router.push('/');
  } catch (error) {
    console.error(
      "Error during sign up:",
      error.response ? error.response.data : error
    );
  } finally {
    isSubmitting.value = false;
  }
};
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
  background-color: #4caf50;
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
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
