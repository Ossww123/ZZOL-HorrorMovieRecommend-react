<!-- ProfileView.vue -->
<template>
  <div class="profile-container">
    <h1 class="text-center text-2xl font-bold mb-4">프로필 정보</h1>

    <!-- 프로필 이미지 -->
    <div class="profile-image-container mb-4">
      <img
        :src="userProfileImage"
        alt="Profile Image"
        class="w-32 h-32 rounded-full mx-auto border-2 border-white"
      />
    </div>

    <!-- 사용자 정보 -->
    <div class="profile-info text-center">
      <p class="text-lg font-semibold">닉네임: {{ nickname }}</p>
      <p class="text-lg font-semibold">이메일: {{ email }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter"; // store 가져오기

// store에서 필요한 데이터 가져오기
const store = useCounterStore();

// 컴포넌트가 마운트되면 fetchUserProfile 호출하여 정보 불러오기
onMounted(() => {
  store.fetchUserProfile();
});

// 프로필 이미지, 닉네임, 이메일을 computed로 반환
const userProfileImage = computed(
  () => store.profileImage || "default-profile.png"
);
const nickname = computed(() => store.nickname || "알 수 없음");
const email = computed(() => store.email || "이메일 없음");
</script>

<style scoped>
.profile-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #1f2937; /* 배경색 */
  border-radius: 8px;
  color: white;
}

.profile-image-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profile-info p {
  margin: 10px 0;
}
</style>
