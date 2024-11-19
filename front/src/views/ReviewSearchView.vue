<template>
  <div class="review-search-view">
    <input v-model="searchQuery" @input="fetchReviews" placeholder="영화 제목을 입력하세요" />
    <div v-if="loading" class="loading">검색 중...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="videos.length === 0 && !loading" class="no-results">결과가 없습니다.</div>
    <div class="youtube-cards">
      <YoutubeCard
        v-for="video in videos"
        :key="video.id.videoId"
        :video="video"
        @click="openModal(video.id.videoId)"
      />
    </div>

    <YoutubeReviewModal v-if="modalVisible" :videoId="selectedVideoId" @close="closeModal" />
  </div>
</template>

<script>
import axios from 'axios';  // axios 임포트
import YoutubeCard from '@/components/YoutubeCard.vue';
import YoutubeReviewModal from '@/components/YoutubeReviewModal.vue';

export default {
  components: {
    YoutubeCard,
    YoutubeReviewModal,
  },
  data() {
    return {
      searchQuery: '',
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
        const response = await axios.get('https://www.googleapis.com/youtube/v3/search', {
          params: {
            part: 'snippet',
            q: `${this.searchQuery} 리뷰`,
            type: 'video',
            key: import.meta.env.VITE_YOUTUBE,  // 실제 API 키를 입력해야 합니다.
          },
        });

        // 가져온 영상을 videos 배열에 저장
        this.videos = response.data.items;
      } catch (err) {
        this.error = '영화 리뷰를 불러오는 데 실패했습니다.';
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
}
.loading {
  font-size: 16px;
}
.error {
  color: red;
}
.no-results {
  font-size: 16px;
  color: gray;
}
.youtube-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style>
