<template>
  <div class="review-search-view">
    <input
      v-model="searchQuery"
      @input="fetchReviews"
      placeholder="영화 제목을 입력하세요"
      class="search-input"
    />
    <div v-if="loading" class="loading">검색 중...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="videos.length === 0 && !loading" class="no-results">
      결과가 없습니다.
    </div>
    <div class="youtube-cards">
      <YoutubeCard
        v-for="video in videos"
        :key="video.id.videoId"
        :video="video"
        @click="openModal(video.id.videoId)"
        class="youtube-card"
      />
    </div>

    <YoutubeReviewModal
      v-if="modalVisible"
      :videoId="selectedVideoId"
      @close="closeModal"
    />
  </div>
</template>

<script>
import axios from "axios"; // axios 임포트
import YoutubeCard from "@/components/YoutubeCard.vue";
import YoutubeReviewModal from "@/components/YoutubeReviewModal.vue";

export default {
  components: {
    YoutubeCard,
    YoutubeReviewModal,
  },
  data() {
    return {
      searchQuery: "",
      videos: [],
      loading: false,
      error: null,
      modalVisible: false,
      selectedVideoId: null,
    };
  },
  methods: {
    // 영화 제목을 입력받아 리뷰 영상을 검색
    async fetchReviews() {
      if (!this.searchQuery.trim()) return;

      this.loading = true;
      this.error = null;

      try {
        // axios를 사용하여 API 호출
        const response = await axios.get(
          "https://www.googleapis.com/youtube/v3/search",
          {
            params: {
              part: "snippet",
              q: `${this.searchQuery} 리뷰`,
              type: "video",
              key: import.meta.env.VITE_YOUTUBE, // 실제 API 키를 입력해야 합니다.
            },
          }
        );

        // 가져온 영상을 videos 배열에 저장
        this.videos = response.data.items;
      } catch (err) {
        this.error = "영화 리뷰를 불러오는 데 실패했습니다.";
      } finally {
        this.loading = false;
      }
    },
    // 모달을 열고 선택한 영상 ID를 전달
    openModal(videoId) {
      this.selectedVideoId = videoId;
      this.modalVisible = true;
    },
    // 모달을 닫는 함수
    closeModal() {
      this.modalVisible = false;
      this.selectedVideoId = null;
    },
  },
};
</script>

<style scoped>
.review-search-view {
  padding: 20px;
  background-color: #2d3748; /* Dark background */
  color: white;
  border-radius: 8px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  margin-bottom: 20px;
  background-color: #1a202c;
  color: white;
  border: 1px solid #4a5568;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #e53e3e;
  outline: none;
}

.loading {
  font-size: 16px;
  color: #e53e3e; /* Red color for loading */
}

.error {
  color: #e53e3e;
  font-size: 16px;
  margin-top: 10px;
}

.no-results {
  font-size: 16px;
  color: gray;
  margin-top: 10px;
}

.youtube-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-top: 20px;
}

.youtube-card {
  width: 300px;
  background-color: #1a202c;
  padding: 15px;
  border-radius: 8px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.youtube-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.youtube-card img {
  width: 100%;
  border-radius: 8px;
}

.youtube-card h3 {
  margin-top: 10px;
  font-size: 18px;
  font-weight: bold;
}

.youtube-card p {
  font-size: 14px;
  color: #cbd5e0;
  margin-top: 5px;
}

/* Modal styles */
.youtube-review-modal {
  background-color: rgba(0, 0, 0, 0.8);
  padding: 20px;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .youtube-cards {
    flex-direction: column;
    align-items: center;
  }

  .youtube-card {
    width: 90%;
  }
}
</style>
