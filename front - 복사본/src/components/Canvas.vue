<template>
  <div ref="canvasWrapper" class="canvas-wrapper flex">
    <!-- 캔버스 영역 -->
    <div class="canvas-container flex-1">
      <canvas ref="canvas" class="rounded-lg shadow-lg"></canvas>
    </div>

    <!-- 영화 정보 영역 -->
    <div
      class="movie-info flex flex-col justify-between p-4 bg-gray-800 text-white"
    >
      <h2 class="text-2xl font-semibold text-red-600 mb-4">
        {{ featuredMovie.title }}
      </h2>
      <p class="text-base mb-4">{{ featuredMovie.overview }}</p>
      <button
        class="bg-red-600 px-4 py-2 rounded-lg text-white hover:bg-red-700 transition duration-300"
        @click="goToMoviePage"
      >
        정보 페이지
      </button>
    </div>
  </div>

  <!-- 새로운 이전/다음 버튼 -->
  <div class="navigation-buttons flex justify-center gap-4 mt-4">
    <button
      @click="rotateCounterClockwise"
      class="px-6 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition duration-300"
    >
      이전
    </button>
    <button
      @click="rotateClockwise"
      class="px-6 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition duration-300"
    >
      다음
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps, computed } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
  movies: {
    type: Array,
    required: true,
  },
});

const router = useRouter();
const canvas = ref(null);
const canvasWrapper = ref(null);
const images = ref([]);
const angle = ref(0);
const targetAngle = ref(0);
let animationFrameId = null;

// 3시 방향의 영화 인덱스를 추적
const featuredMovieIndex = ref(0);

// 3시 방향의 영화 정보
const featuredMovie = computed(() => {
  return props.movies[featuredMovieIndex.value];
});

const goToMoviePage = () => {
  const movieId = featuredMovie.value.id;
  router.push({ name: "MovieDetailView", params: { movie_id: movieId } });
};

const resizeCanvas = () => {
  if (canvasWrapper.value && canvas.value) {
    const width = canvasWrapper.value.clientWidth;
    const height = canvasWrapper.value.clientHeight;
    canvas.value.width = width;
    canvas.value.height = height;
  }
};

const rotateClockwise = () => {
  targetAngle.value += (2 * Math.PI) / 5;
  featuredMovieIndex.value =
    (featuredMovieIndex.value - 1 + props.movies.length) % props.movies.length;

  animateRotation();
};

const rotateCounterClockwise = () => {
  targetAngle.value -= (2 * Math.PI) / 5;
  featuredMovieIndex.value =
    (featuredMovieIndex.value + 1) % props.movies.length;
  animateRotation();
};

const animateRotation = () => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }

  const rotateStep = 0.05;

  const rotate = () => {
    const diff = targetAngle.value - angle.value;

    if (Math.abs(diff) < rotateStep) {
      angle.value = targetAngle.value;
    } else {
      angle.value += rotateStep * Math.sign(diff);
    }

    draw();
    animationFrameId = requestAnimationFrame(rotate);
  };

  rotate();
};

onMounted(() => {
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);
  loadImages();
});

watch([images, angle], () => {
  if (images.value.length > 0) {
    draw();
  }
});

const draw = () => {
  if (!canvas.value) return;
  const ctx = canvas.value.getContext("2d");
  const width = canvas.value.width;
  const height = canvas.value.height;
  ctx.clearRect(0, 0, width, height);

  ctx.save();
  ctx.translate(-width / 8, height / 2); // 캔버스 중앙으로 이동
  ctx.rotate(angle.value);

  const radiusX = Math.min(width, height) * 1.1; // 가로 반경
  const radiusY = Math.min(width, height) * 1.1; // 세로 반경 (원하는 비율로 수정 가능)

  images.value.forEach((image, index) => {
    ctx.save();
    const angleOffset = (index * Math.PI * 2) / images.value.length;
    const x = radiusX * Math.cos(angleOffset); // 가로 반경에 맞춰 x 좌표 계산
    const y = radiusY * Math.sin(angleOffset); // 세로 반경에 맞춰 y 좌표 계산
    ctx.translate(x, y);
    ctx.rotate(angleOffset);

    const imageAspectRatio = (image.width / image.height) * 1.2;
    let imageWidth = image.width;
    let imageHeight = image.height;

    // 비율을 맞춰 크기 계산
    if (imageWidth > imageHeight) {
      imageHeight = imageWidth / imageAspectRatio;
    } else {
      imageWidth = imageHeight * imageAspectRatio;
    }

    ctx.drawImage(
      image,
      -imageWidth / 3, // 이미지의 중심을 맞추기 위해 수정
      -imageHeight / 3, // 이미지의 중심을 맞추기 위해 수정
      imageWidth / 1.2,
      imageHeight / 1.5
    );
    ctx.restore();
  });

  ctx.restore();
};

const loadImages = () => {
  images.value = [];
  let loadedImages = 0;

  props.movies.forEach((movie) => {
    const img = new Image();
    img.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
    img.onload = () => {
      images.value.push(img);
      loadedImages++;
      if (loadedImages === props.movies.length) {
        draw();
      }
    };
  });
};
</script>

<!-- 이전 스타일 코드 동일 -->

<style scoped>
.canvas-wrapper {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 500px;
}

.canvas-container {
  flex: 1;
  position: relative;
}

button {
  background-color: #ff9a9a;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #c53030;
}

canvas {
  width: 100%;
  height: 100%;
}

.movie-info {
  width: 30vw; /* 화면 가로 크기의 30% */
  padding: 20px;
  background-color: #1a202c;
  color: white;
  flex-shrink: 0; /* 영화 정보 영역이 축소되지 않도록 설정 */
  max-width: 400px; /* 최대 너비 설정 (필요시 조정) */
}

.movie-info h2 {
  font-size: 1.5rem;
  font-weight: bold;
}

.movie-info p {
  margin-top: 1rem;
  font-size: 1rem;
}

.movie-info button {
  margin-top: 2rem;
  padding: 10px 20px;
  background-color: #e53e3e;
  border-radius: 5px;
  text-transform: uppercase;
  transition: background-color 0.3s;
}

.movie-info button:hover {
  background-color: #c53030;
}

.navigation-buttons {
  margin-top: 1rem;
}
</style>
