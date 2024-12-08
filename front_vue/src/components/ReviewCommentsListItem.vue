<template>
  <div>
    <h5>{{ comment.user.nickname }}</h5>
    <div v-if="!isEditing">
      <p>{{ props.comment.content }}</p>
      <button @click="startEdit">수정</button>
      <button @click="deleteComment(props.review_pk, props.comment.id)">삭제</button>
    </div>
    <div v-else>
      <textarea v-model="editedContent"></textarea>
      <button @click="updateComment(props.review_pk, props.comment.id)">저장</button>
      <button @click="cancelEdit">취소</button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';
import { ref } from 'vue';

const store = useCounterStore();
const editedContent = ref('');
const isEditing = ref(false);

const props = defineProps({
  review_pk: String,
  comment: Object
})

const deleteComment = function (review_pk, comment_Id) {
  axios.delete(`${store.API_URL}/api/v1/${review_pk}/comments/${comment_Id}/`, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getReviewComments(review_pk)
    })
    .catch(console.error)
}

const startEdit = () => {
  editedContent.value = props.comment.content;
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
  editedContent.value = '';
};

const updateComment = function (review_pk, comment_Id) {
  axios.put(`${store.API_URL}/api/v1/${review_pk}/comments/${comment_Id}/`, { content: editedContent.value }, {
    headers: { Authorization: `Token ${store.token}` }
  })
    .then(() => {
      store.getReviewComments(review_pk);
      isEditing.value = false;
    })
    .catch(console.error);
};
</script>

<style scoped>
div {
  background-color: #2c2c2c;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 12px;
  color: #fff;
}

h5 {
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

button {
  background-color: #570000;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 8px;
}

button:hover {
  background-color: #740000;
}
</style>
