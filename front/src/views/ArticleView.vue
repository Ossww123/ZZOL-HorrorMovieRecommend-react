<!-- ArticleView.vue -->
<template>
  <div
    class="main-container bg-black text-white relative"
    @mousemove="moveImage"
  >
    <!-- 좌측 움직이는 이미지 -->
    <img
      src="@/assets/ghost1.png"
      alt="Left Ghost"
      :style="{
        transform: `translate(${imagePosition1.x}px, ${imagePosition1.y}px)`,
        width: `${imageWidth}vw`,
        left: `${sideSpace}px`,
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
        right: `${sideSpace}px`,
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
        left: `${sideSpace}px`,
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
        right: `${sideSpace}px`,
      }"
      class="absolute z-10"
    />

    <div :style="containerStyle" class="content-container">
      <h1>정보 게시판</h1>
      <div class="search-create-container">
        <!-- 검색창 -->
        <div class="search-box">
          <input
            type="text"
            v-model="searchKeyword"
            @input="handleSearch"
            placeholder="검색어를 입력하세요"
          />
        </div>
        <!-- Create 버튼 -->
        <RouterLink :to="{ name: 'CreateView' }" class="create-link"
          >Create</RouterLink
        >
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
const sideSpace = ref(20); // 사이드 공간 기본값 설정

// Store와 검색 처리
const store = useCounterStore();
const searchKeyword = ref("");
const filteredArticles = ref([]);

// 이미지 움직임 함수
const moveImage = (event) => {
  const { clientX, clientY } = event;
  const scrollY = window.scrollY;

  // 이미지 움직임 범위 제한
  const maxMove = window.innerWidth * 0.05; // 최대 이동 거리는 화면 너비의 5%

  // 왼쪽 이미지 x, y 위치 계산
  const leftX = (clientX - window.innerWidth / 2) / 15 - window.innerWidth / 20;
  imagePosition1.value.x = Math.min(Math.max(leftX, -maxMove), maxMove);
  imagePosition3.value.x = Math.min(Math.max(leftX, -maxMove), maxMove);

  // 오른쪽 이미지 x, y 위치 계산
  const rightX =
    (clientX - window.innerWidth / 2) / 15 + window.innerWidth / 20;
  imagePosition2.value.x = Math.min(Math.max(rightX, -maxMove), maxMove);
  imagePosition4.value.x = Math.min(Math.max(rightX, -maxMove), maxMove);

  // y 위치는 동일하게 유지
  imagePosition1.value.y =
    (clientY - window.innerHeight / 2) / 10 +
    scrollY * 1 +
    window.innerHeight / 10;
  imagePosition2.value.y =
    (clientY - window.innerHeight / 2) / 10 +
    scrollY * 1 +
    window.innerHeight / 10;
  imagePosition3.value.y =
    (clientY - window.innerHeight / 2) / 10 +
    scrollY * 1 +
    window.innerHeight / 2;
  imagePosition4.value.y =
    (clientY - window.innerHeight / 2) / 10 +
    scrollY * 1 +
    window.innerHeight / 2;
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
    width: "100%",
    margin: "0 auto",
    padding: `0 ${sideSpace.value * 1.5}px`, // Adjusting padding for side space
  };
});

// 검색 처리
const handleSearch = debounce(async () => {
  const results = await store.searchArticles(searchKeyword.value);
  filteredArticles.value = results;
}, 300);

onMounted(async () => {
  await store.getArticles(); // 먼저 전체 게시글을 가져옴
  handleSearch(); // 그 다음 검색 처리
});

// 화면 크기에 따른 이미지 크기 조정
const updateImageSize = () => {
  const width = window.innerWidth;
  imageWidth.value = Math.min(width * 0.08, 10); // 최대 10vw, 화면 너비의 8%
};

window.addEventListener("resize", () => {
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
  max-width: 1200px; /* 최대 너비 지정 */
  margin: 0 auto;
  padding: 30px 20px; /* 여백 추가 */
  border-radius: 10px; /* 둥근 모서리 */
}

h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #fff; /* 글자색을 하얗게 */
  text-align: center;
}

.create-link {
  display: inline-block;
  margin-bottom: 30px;
  padding: 12px 20px;
  font-size: 1.2rem;
  background-color: #f56565; /* 붉은색 */
  color: white;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.create-link:hover {
  background-color: #e53e3e;
  transform: translateY(-2px); /* 약간 올라가는 효과 */
}

.create-link:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.8); /* 포커스 시 테두리 강조 */
}

.search-box {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.search-box input {
  width: 60%;
  padding: 12px 20px;
  font-size: 1.1rem;
  border: 1px solid #f56565; /* 붉은색 테두리 */
  border-radius: 8px;
  background-color: #333;
  color: white;
  transition: border-color 0.3s;
}

.search-box input:focus {
  border-color: #e53e3e; /* 포커스 시 테두리 색상 변경 */
  outline: none;
}

.search-box input::placeholder {
  color: #aaa; /* 플레이스홀더 색상 */
}

.article-list-container {
  margin-top: 20px;
  padding-top: 10px;
}

.article-list-container ul {
  list-style: none;
  padding-left: 0;
}

.article-list-container li {
  margin-bottom: 10px;
  padding: 20px;
  border-radius: 8px;
}

.article-list-container li:hover {
  background-color: #333; /* 호버 시 밝아지는 효과 */
}

.article-list-container h2 {
  font-size: 1.8rem;
  color: #f56565; /* 제목 색상 */
  margin-bottom: 10px;
}

.article-list-container p {
  color: #ccc; /* 본문 색상 */
  font-size: 1rem;
}

@media screen and (max-width: 768px) {
  .search-box input {
    width: 80%; /* 모바일에서는 검색창 크기 축소 */
  }

  .content-container {
    padding: 20px 10px;
  }
}
</style>
