<template>
  <div>
    <form @submit.prevent="createComment(review_pk)">
      <!-- 내용 입력 -->
      <div>
          <h3>댓글 작성란</h3>
          <label for="content">내용 : </label>
          <textarea id="content" v-model.trim="content"></textarea>
        </div>
        <input type="submit" value="제출">
        <hr>
    </form>
    <ReviewCommentsListItem
    v-for="comment in store.comments"
    :key="comment.id"
    :comment="comment"
    :review_pk="review_pk"
    />
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

onMounted(async () =>{
  store.getReviewComments(props.review_pk)
})

const createComment = function (review_pk) {
  console.log(store.token)
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/${review_pk}/comments/`,
    data: {
      content: content.value
    },
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((res) => {
    console.log('댓글 생성됨!')
    content.value = ''
    store.getReviewComments(review_pk)
  })
  .catch((err) => {
    if (err.response.data.error) {
    alert(err.response.data.error)
    }
  })
}




</script>

<style scoped>

</style>