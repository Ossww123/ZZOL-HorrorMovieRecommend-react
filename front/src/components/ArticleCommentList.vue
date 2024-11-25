<template>
  <div>
    <form @submit.prevent="createComment(props.article.id)">
      <!-- 내용 입력 -->
      <div>
          <h3>댓글 작성란</h3>
          <label for="content">내용 : </label>
          <textarea id="content" v-model.trim="content"></textarea>
        </div>
        <input type="submit" value="제출">
        <hr>
    </form>
    <ArticleCommentListItem
    v-for="comment in store.articleComments"
    :key="comment.id"
    :comment="comment"
    :article_pk="props.article.id"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import ArticleCommentListItem from './ArticleCommentListItem.vue';
import axios from 'axios';

const store = useCounterStore()
const content = ref(null)


const props = defineProps({
  article: Object,
})

onMounted(async () =>{
  store.getArticleComments(props.article.id)
  console.log(props.article.id)
})

const createComment = function (article_id) {
  console.log(store.token)
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/articles/${article_id}/comments/`,
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
    store.getArticleComments(article_id)
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