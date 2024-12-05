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
    <!-- 중앙에 배치된 콘텐츠를 감싸는 컨테이너 -->
    <div :style="containerStyle" class="content-container">
      <Welcome />
      <MovieRecommend />
      <Home_RandomTest class="z-20" />
      <Home_PopularLatestTest class="z-20" />
      <RandomTrailer />
    </div>
  </div>
</template>

<script setup>
import MovieRecommend from '@/components/MovieRecommend.vue';
import Home_RandomTest from '@/components/Home_RandomTest.vue';
import { ref, computed } from 'vue';
import RandomTrailer from '@/components/RandomTrailer.vue';
import Home_PopularLatestTest from '@/components/Home_PopularLatestTest.vue';
import Welcome from '@/components/Welcome.vue';

const imagePosition1 = ref({ x: 0, y: 0 });
const imagePosition2 = ref({ x: 0, y: 0 });
const imagePosition3 = ref({ x: 0, y: 0 });
const imagePosition4 = ref({ x: 0, y: 0 });
const imageWidth = ref(10);

// 화면 크기에 따른 사이드 여백 계산
const sideSpace = computed(() => {
  const width = window.innerWidth;
  return Math.max(width * 0.05, 20); // 최소 20px, 화면 너비의 5%
});

const moveImage = (event) => {
  const { clientX, clientY } = event;
  const scrollY = window.scrollY;

  // 이미지 움직임 범위를 제한하여 컨텐츠를 덜 가리도록 조정
  const maxMove = window.innerWidth * 0.05; // 최대 이동 거리를 화면 너비의 5%로 제한

  // 왼쪽 이미지 x, y 위치 계산
  const leftX = ((clientX - window.innerWidth / 2) / 15) - window.innerWidth / 20;
  imagePosition1.value.x = Math.min(Math.max(leftX, -maxMove), maxMove);
  imagePosition3.value.x = Math.min(Math.max(leftX, -maxMove), maxMove);

  // 오른쪽 이미지 x, y 위치 계산
  const rightX = ((clientX - window.innerWidth / 2) / 15) + window.innerWidth / 20;
  imagePosition2.value.x = Math.min(Math.max(rightX, -maxMove), maxMove);
  imagePosition4.value.x = Math.min(Math.max(rightX, -maxMove), maxMove);

  // y 위치는 동일하게 유지
  imagePosition1.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight/10;
  imagePosition2.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight/10;
  imagePosition3.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight / 2;
  imagePosition4.value.y = (clientY - window.innerHeight / 2) / 10 + scrollY * 1 + window.innerHeight / 2;
};

const containerStyle = computed(() => {
  const width = window.innerWidth;
  let containerWidth = 1500;
  
  if (width < 1500) {
    containerWidth = width * 0.67;
  } else if (width < 1200) {
    containerWidth = width * 0.67;
  }

  // 양쪽 패딩을 추가하여 이미지를 위한 공간 확보
  const sidePadding = `${sideSpace.value * 1.5}px`;

  return {
    maxWidth: `${containerWidth}px`,
    width: '100%',
    margin: '0 auto',
    padding: `0 ${sidePadding}`, // 양쪽 패딩 추가
  };
});

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
  min-height: 100vh;
  background-color: black;
  width: 100%;
  height: 100%;
}

img {
  transition: transform 0.1s ease-out;
}

.content-container {
  position: relative;
  width: 100%;
  margin: 0 auto;
}

.MovieRecommend, .Home_RandomTest, .RandomTrailer {
  width: 100%;
  height: 100%;
}
</style>