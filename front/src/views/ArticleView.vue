<template>
  <div class="main-container bg-black text-white relative" @mousemove="moveImage">
    <!-- 좌측 움직이는 이미지 -->
    <img
      src="@/assets/ghost1.png"
      alt="Left Ghost"
      :style="{
        transform: `translate(${imagePosition1.x}px, ${imagePosition1.y}px)`,
        width: `${imageWidth}vw`,
        left: `${sideSpace}px`
      }"
      class="absolute z-10"
    />

    <!-- 우측 움직이는 이미지 -->
    <img
      src="@/assets/ghost2.png"
      alt="Right Ghost"
      :style="{
        transform: `translate(${imagePosition2.x}px, ${imagePosition2.y}px)`,
        width: `${imageWidth}vw`,
        right: `${sideSpace}px`
      }"
      class="absolute z-10"
    />

    <!-- 좌측 움직이는 이미지 2 -->
    <img
      src="@/assets/ghost2.png"
      alt="Left Ghost"
      :style="{
        transform: `translate(${imagePosition3.x}px, ${imagePosition3.y}px)`,
        width: `${imageWidth}vw`,
        left: `${sideSpace}px`
      }"
      class="absolute z-10"
    />

    <!-- 우측 움직이는 이미지 2 -->
    <img
      src="@/assets/ghost1.png"
      alt="Right Ghost"
      :style="{
        transform: `translate(${imagePosition4.x}px, ${imagePosition4.y}px)`,
        width: `${imageWidth}vw`,
        right: `${sideSpace}px`
      }"
      class="absolute z-10"
    />

    <div :style="containerStyle" class="content-container">
      <h1>Article Page</h1>
      <RouterLink :to="{ name: 'CreateView' }" class="create-link">Create</RouterLink>
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchKeyword"
          @input="handleSearch"
          placeholder="검색어를 입력하세요"
        />
      </div>
      <ArticleList :articles="filteredArticles" />
    </div>
  </div>
</template>

<script setup>
import ArticleList from "@/components/ArticleList.vue";
import { onMounted, ref, watch, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import { RouterLink } from "vue-router";
import { debounce } from "lodash";

// 이미지 위치와 크기 설정
const imagePosition1 = ref({ x: 0, y: 0 });
const imagePosition2 = ref({ x: 0, y: 0 });
const imagePosition3 = ref({ x: 0, y: 0 });
const imagePosition4 = ref({ x: 0, y: 0 });

const imageWidth = ref(10);
const sideSpace = ref(20);  // 사이드 공간 기본값 설정

// Store와 검색 처리
const store = useCounterStore();
const searchKeyword = ref('');
const filteredArticles = ref([]);

// 이미지 움직임 함수
const moveImage = (event) => {
  const { clientX, clientY } = event;
  const scrollY = window.scrollY;

  // 이미지 움직임 범위 제한
  const maxMove = window.innerWidth * 0.05; // 최대 이동 거리는 화면 너비의 5%

  // 왼쪽 이미지 x, y 위치 계산
  const leftX = ((clientX - window.innerWidth / 2) / 15) - window.innerWidth / 20;
  imagePosition1.value.x = Math.min(Math.max(leftX, -maxMove), maxMove);
  imagePosition3.value.x = Math.min(Math.max(leftX, -maxMove), maxMove);

  // 오른쪽 이미지 x, y 위치 계산
  const rightX = ((clientX - window.innerWidth / 2) / 15) + window.innerWidth / 20;
  imagePosition2.value.x = Math.min(Math.max(rightX, -maxMove), maxMove);
  imagePosition4.value.x = Math.min(Math.max(rightX, -maxMove), maxMove);

  // y 위치는 동일하게 유지
  imagePosition1.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight / 10;
  imagePosition2.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight / 10;
  imagePosition3.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight / 2;
  imagePosition4.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight / 2;
};

// 컨테이너 스타일 계산
const containerStyle = computed(() => {
  const width = window.innerWidth;
  let containerWidth = 1500;

  if (width < 1500) {
    containerWidth = width * 0.67;
  } else if (width < 1200) {
    containerWidth = width * 0.67;
  }

  // 사이드 공간 계산
  sideSpace.value = Math.max(width * 0.05, 20);

  return {
    maxWidth: `${containerWidth}px`,
    width: '100%',
    margin: '0 auto',
    padding: `0 ${sideSpace.value * 1.5}px`, // Adjusting padding for side space
  };
});

// 검색 처리
const handleSearch = debounce(async () => {
  const results = await store.searchArticles(searchKeyword.value);
  filteredArticles.value = results;
}, 300);

onMounted(async () => {
  await store.getArticles() // 먼저 전체 게시글을 가져옴
  handleSearch() // 그 다음 검색 처리
})

// 화면 크기에 따른 이미지 크기 조정
const updateImageSize = () => {
  const width = window.innerWidth;
  imageWidth.value = Math.min(width * 0.08, 10); // 최대 10vw, 화면 너비의 8%
};

window.addEventListener('resize', () => {
  updateImageSize();
});

// 초기 이미지 크기 설정
updateImageSize();
</script>

<style scoped>
.main-container {
  position: relative;
  width: 100%;
  height: 100vh;
}

.content-container {
  position: relative;
  width: 100%;
  margin: 0 auto;
}
</style>
