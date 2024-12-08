<template>
  <h1>안녕하세요! {{ nickname }}님!</h1>
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

const nickname = computed(() => store.nickname || "알 수 없음");
</script>

<style scoped>
h1 {
  text-align: center; /* 텍스트를 가로로 가운데 정렬 */
  font-size: 3em; /* 글씨 크기 키우기 (필요에 따라 크기 조절) */
}
</style>
