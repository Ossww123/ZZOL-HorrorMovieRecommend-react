<template>
  <div>
    <h5>닉네임 : {{ comment.user.nickname }}</h5>
    <p>content: {{ comment.content }}</p>
    <button @click="deleteComment(review_pk, comment.id)">삭제</button>
    <hr>
  </div>
</template>

<script setup>
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';


const store = useCounterStore();


defineProps({
  review_pk: {
    type: String,
    required: true
  },
  comment: Object
})

const deleteComment = function (review_pk, comment_Id) {
  axios({
        method: 'delete'  ,
        url: `${store.API_URL}/api/v1/${review_pk}/comments/${comment_Id}/` , 
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      .then((res) => {
        console.log("댓글 삭제됨")
        store.getReviewComments(review_pk)
      })
      .catch((err) => {
        console.log("댓글 삭제 안됨..")
        console.log(err)
      })
    }


</script>

<style scoped>

</style>