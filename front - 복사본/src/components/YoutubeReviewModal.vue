<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal">
      <button class="close-btn" @click="close">×</button>
      <iframe
        :src="`https://www.youtube.com/embed/${videoId}?autoplay=1`"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen
        class="video-frame"
      ></iframe>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    videoId: String,
  },
  methods: {
    close() {
      this.$emit('close');
    },
  },
};
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
  z-index: 1000;
}
.modal {
  position: relative;
  background: white;
  padding: 20px;
  width: 80%;
  max-width: 800px;
}
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #333;
}
.video-frame {
  width: 100%;
  height: 450px;
}
</style>
