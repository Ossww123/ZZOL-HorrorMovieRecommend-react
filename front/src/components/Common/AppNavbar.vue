<template>
  <nav class="bg-black text-white p-4 flex items-center">
    <!-- 로고 이미지 추가 -->
    <RouterLink :to="{ name: 'HomeView' }">
      <img src="@/assets/logo.png" alt="Logo" class="h-16 mr-4" />
    </RouterLink>

    <!-- 네비게이션 링크들 왼쪽 정렬 -->
    <div class="flex space-x-6">
      <RouterLink :to="{ name: 'HomeView' }" class="hover:text-gray-400"
        >Home</RouterLink
      >
      <RouterLink :to="{ name: 'ArticleView' }" class="hover:text-gray-400"
        >Articles</RouterLink
      >
      <RouterLink to="/movies" class="hover:text-gray-400">Movies</RouterLink>

      <!--
      <RouterLink to="/review-search" class="hover:text-gray-400"
        >리뷰 검색</RouterLink
      >
      <RouterLink to="/recommended" class="hover:text-gray-400"
        >영화 추천</RouterLink
      >
      <RouterLink to="/random" class="hover:text-gray-400">랜덤</RouterLink>

      -->
    </div>

    <!-- 로그인 상태에 따라 검색 창 위치 조정 -->
    <div class="ml-auto flex items-center space-x-4">
      <!-- 로그인하지 않았을 때 검색 창을 로그인 버튼 왼쪽에 위치 -->
      <div v-if="!isLoggedIn" class="flex items-center">
        <input
          type="text"
          v-model="searchQuery"
          @input="onSearch"
          placeholder="영화 제목 검색"
          class="px-4 py-2 rounded bg-gray-800 text-white focus:outline-none"
        />
      </div>

      <!-- 로그인, 회원가입 버튼들 -->
      <RouterLink
        v-if="!isLoggedIn"
        :to="{ name: 'LogInView' }"
        class="hover:text-gray-400"
        >로그인</RouterLink
      >
      <RouterLink
        v-if="!isLoggedIn"
        :to="{ name: 'SignUpView' }"
        class="hover:text-gray-400"
        >회원가입</RouterLink
      >

      <!-- 로그인 상태에서 -->
      <div v-if="isLoggedIn" class="flex items-center space-x-4">
        <!-- 검색 창 -->
        <input
          type="text"
          v-model="searchQuery"
          @input="onSearch"
          placeholder="영화 제목 검색"
          class="px-4 py-2 rounded bg-gray-800 text-white focus:outline-none"
        />

        <!-- 로그아웃 버튼 -->
        <form @submit.prevent="logOut">
          <input
            type="submit"
            value="Logout"
            class="hover:text-gray-400 py-2 px-4 rounded border border-transparent bg-transparent text-white cursor-pointer"
          />
        </form>

        <!-- 프로필 정보 링크 -->
        <RouterLink to="/profile" class="hover:text-gray-400">
          <img
            :src="userProfileImage"
            alt="Profile"
            class="w-8 h-8 rounded-full border-2 border-white"
          />
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter, useRoute } from "vue-router"; // useRouter를 가져옴
import { debounce } from "lodash";

// 스토어와 라우터 훅을 설정
const store = useCounterStore();
const router = useRouter(); // useRouter 훅으로 라우터 객체를 가져옴
const route = useRoute();
const searchQuery = ref(""); // 검색어 상태 변수

// 검색 함수 (디바운스 적용)
const onSearch = debounce(() => {
  console.log("검색어:", searchQuery.value);
  // searchQuery가 있을 때 MovieListView로 쿼리 파라미터로 검색어를 넘기기
  if (searchQuery.value) {
    router.push({
      name: "MovieListView",
      query: { search: searchQuery.value },
    });
  }
}, 500);

onMounted(() => {
  // 라우터 쿼리 파라미터에 "search"가 없을 경우에만 검색어를 초기화
  if (!route.query.search) {
    searchQuery.value = "";
  }
});

// 로그아웃 함수
const logOut = function () {
  store.logOut();
};

// 로그인 여부를 computed로 처리
const isLoggedIn = computed(() => store.isLogin);

import defaultProfileImage from "@/assets/default-profile.png";

// 프로필 이미지 경로를 조건에 따라 선택
const userProfileImage = computed(() => {
  console.log("Profile Image URL:ㄴㄴㄴㄴ", store.profileImage);
  console.log("한번더", store.profileImage);
  // profileImage가 유효하면 그대로 사용
  if (store.profileImage) {
    console.log("여기 안 왔어?");
    return store.profileImage; // 절대 URL이므로 그대로 반환
  }
  return defaultProfileImage; // 기본 이미지 반환
});
</script>
