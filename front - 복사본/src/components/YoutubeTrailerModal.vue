<!--YoutubeTrailerModal.vue-->
<template>
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <button @click="closeModal" class="close-btn">닫기</button>
      <h2>{{ movie.original_title }} 공식 예고편</h2>
      <iframe
        :src="`https://www.youtube.com/embed/${videoId}?autoplay=1`"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen
        width="560"
        height="315"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Props passed from parent component
const props = defineProps({
  movie: Object, // Pass the YouTube API key as a prop
});

// State variables
const videoId = ref(null);
const showModal = ref(true); // Assuming you control this from a parent component
const youtubeApiKey = import.meta.env.VITE_YOUTUBE

// Function to fetch the official trailer from YouTube
async function fetchTrailer() {
  try {

    const response = await axios.get(
      `https://www.googleapis.com/youtube/v3/search`, {
        params: {
          part: 'snippet',
          q: `${props.movie.original_title} official trailer`,
          type: 'video',
          key: youtubeApiKey,
          maxResults: 1,
        }
      }
    );
    
    // Extract video ID from response
    if (response.data.items.length > 0) {
      videoId.value = response.data.items[0].id.videoId;
    } else {
      console.error('No trailer found for this movie.');
    }
  } catch (error) {
    console.error('Error fetching trailer:', error);
  }
}

// Fetch trailer when component mounts
onMounted(() => {
  fetchTrailer();
});

// Function to close modal (assuming this is needed)
function closeModal() {
  showModal.value = false;
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 600px;
}
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}
</style>
