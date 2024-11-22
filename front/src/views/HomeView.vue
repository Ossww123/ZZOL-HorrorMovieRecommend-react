<!-- HomeView.vue -->
<template>
  <div class="bg-black h-screen text-white relative" @mousemove="moveImage">
    <!-- 중앙에 배치된 텍스트 -->
    <p class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <span class="text-red-500">공포</span>를 위한<br>
      영화 추천 서비스<br>
      <span class="text-orange-500 text-7xl">ZZOL</span>
    </p>
    
    <!-- 마우스 따라 움직이는 배경 이미지 -->
    <img
      src="@/assets/background3.png"
      alt="Dynamic Image"
      :style="{ transform: `translate(${imagePosition3.x}px, ${imagePosition3.y}px)`, position: 'absolute', top: '50%', left: '50%', transform: `translate(-50%, -50%)` }"
      class="absolute w-full h-full object-cover z-0"
    />
    
    <!-- 마우스 따라 움직이는 다른 이미지들 -->
    <img
      src="@/assets/ghost1.png"
      alt="Dynamic Image"
      :style="{ transform: `translate(${imagePosition1.x}px, ${imagePosition1.y}px)` }"
      class="absolute w-64 h-96 z-10"
    />
    <img
      src="@/assets/ghost2.png"
      alt="Dynamic Image"
      :style="{ transform: `translate(${imagePosition2.x}px, ${imagePosition2.y}px)` }"
      class="absolute w-64 h-96 z-10"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';

const imagePosition1 = ref({ x: (window.innerWidth / 2) - 1030, y: (window.innerHeight / 2) - 520});
const imagePosition2 = ref({ x: (window.innerWidth / 2) + 500, y: (window.innerHeight / 2) - 500});
const imagePosition3 = ref({ x: 0, y: 0 });

const moveImage = (event) => {
  const { clientX, clientY } = event;
  // 화면의 중앙을 기준으로 이미지 위치를 이동
  imagePosition1.value.x = (clientX - window.innerWidth / 2) / 10 + window.innerWidth / 10; // 10은 이동 속도
  imagePosition1.value.y = (clientY - window.innerHeight / 2) / 10 + window.innerHeight / 10;

  imagePosition2.value.x = (clientX - window.innerWidth / 2) / 10 + window.innerWidth / 10 * 7;; // 10은 이동 속도
  imagePosition2.value.y = (clientY - window.innerHeight / 2) / 10 + window.innerHeight / 10;

  imagePosition3.value.x = window.innerWidth / 4 // 10은 이동 속도
  imagePosition3.value.y = (clientY*0.2 - window.innerHeight / 2) / 10 + window.innerHeight / 10;
};
</script>

<style scoped>
/* 이미지가 부드럽게 움직이도록 transition 추가 */
img {
  transition: transform 0.1s ease-out;
}

/* 텍스트를 화면 중앙에 배치 */
p {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10; /* 텍스트가 배경보다 위에 오도록 설정 */
  font-size: 50px;
  text-align: center;
  color: white;
  width: 100%; /* 텍스트가 화면을 가득 채우도록 설정 */
}

/* 공포 텍스트 빨간색 */
.text-red-500 {
  color: red;
}

/* ZZOL 텍스트 주황색, 폰트 크기 70px */
.text-orange-500 {
  color: orange;
}

.text-7xl {
  font-size: 70px;
}
</style>
