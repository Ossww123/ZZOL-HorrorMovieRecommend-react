<template>
  <div>
    <ReviewCommentsListItem
      v-for="comment in store.comments"
      :key="comment.id"
      :comment="comment"
      :review_pk="review_pk"
    />
    <form @submit.prevent="createComment(review_pk)">
      <div>
        <h3>댓글 작성란</h3>
        <label for="content"></label>
        <textarea id="content" v-model.trim="content" placeholder="댓글을 입력하세요"></textarea>
      </div>
      <input type="submit" value="제출">
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import ReviewCommentsListItem from './ReviewCommentsListItem.vue';
import axios from 'axios';

const store = useCounterStore()
const content = ref(null)

const props = defineProps({
  review_pk: {
    type: String,
    required: true
  }
})

onMounted(async () => {
  store.getReviewComments(props.review_pk)
})

const createComment = function (review_pk) {
  axios.post(`${store.API_URL}/api/v1/${review_pk}/comments/`, { content: content.value }, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      content.value = ''
      store.getReviewComments(review_pk)
    })
    .catch((err) => {
      if (err.response?.data?.error) alert(err.response.data.error)
    })
}
</script>

<style scoped>
form {
  background-color: #1d1d1d;
  border-radius: 8px;
  padding: 10px;
  color: #fff;
  margin-bottom: 20px;
}

h3 {
  margin-bottom: 8px;
}

textarea {
  width: 100%;
  background-color: #333;
  color: #fff;
  border: 1px solid #570000;
  border-radius: 5px;
  padding: 8px;
  margin-top: 8px;
  resize: vertical;
}

input[type="submit"] {
  background-color: #570000;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

input[type="submit"]:hover {
  background-color: #740000;
}
</style>
