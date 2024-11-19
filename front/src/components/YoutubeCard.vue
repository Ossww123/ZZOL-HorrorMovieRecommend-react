<template>
  <div class="youtube-card" @click="handleClick">
    <img :src="video.snippet.thumbnails.medium.url" :alt="video.snippet.title" class="thumbnail" />
    <div class="title">{{ video.snippet.title }}</div>
  </div>
</template>

<script>
export default {
  props: {
    video: Object,
  },
  methods: {
    handleClick() {
      this.$emit('click', this.video.id.videoId);
    },
  },
};
</script>

<style scoped>
.youtube-card {
  width: 250px;
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
}
.youtube-card:hover {
  transform: scale(1.05);
}
.thumbnail {
  width: 100%;
  height: 140px;
  object-fit: cover;
}
.title {
  padding: 10px;
  font-size: 14px;
  font-weight: bold;
}
</style>
