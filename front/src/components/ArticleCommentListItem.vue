<template>
  <div>
    <h5>닉네임 : {{ props.comment.user.nickname }}</h5>
    <div v-if="!isEditing">
      <p>content: {{ props.comment.content }}</p>
      <button @click="startEdit">수정</button>
      <button @click="deleteComment(props.article_pk, props.comment.id)">삭제</button>
    </div>
    <div v-else>
      <textarea v-model="editedContent"></textarea>
      <button @click="updateComment(props.article_pk, props.comment.id)">저장</button>
      <button @click="cancelEdit">취소</button>
    </div>
    <hr>
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
  article_pk: String,
  comment: Object
})

const deleteComment = function (article_pk, comment_Id) {
  axios({
        method: 'delete'  ,
        url: `${store.API_URL}/api/v1/articles/${article_pk}/comments/${comment_Id}/` , 
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      .then((res) => {
        console.log("댓글 삭제됨")
        store.getArticleComments(article_pk)
      })
      .catch((err) => {
        console.log("댓글 삭제 안됨..")
        console.log(err)
      })
    }

const startEdit = () => {
  editedContent.value = props.comment.content;
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
  editedContent.value = '';
};

const updateComment = function (article_pk, comment_Id) {
  axios({
    method: 'put',
    url: `${store.API_URL}/api/v1/articles/${article_pk}/comments/${comment_Id}/`,
    data: {
      content: editedContent.value
    },
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((res) => {
    console.log("댓글 수정됨");
    store.getArticleComments(props.article_pk);
    isEditing.value = false;
  })
  .catch((err) => {
    console.log("댓글 수정 실패");
    console.log(err);
  });
};

</script>

<style scoped>

</style>