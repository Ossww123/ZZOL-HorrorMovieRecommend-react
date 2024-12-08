<template>
  <div class="comment-section">
    <!-- 댓글 목록 -->
    <div v-if="store.articleComments.length > 0" class="comment-list">
      <ArticleCommentListItem
        v-for="comment in store.articleComments"
        :key="comment.id"
        :comment="comment"
        :article_pk="props.article.id"
      />
    </div>

    <!-- 댓글이 없을 때 표시 -->
    <p v-else class="no-comments">댓글이 아직 없습니다.</p>

    <!-- 댓글 작성란 -->
    <form
      @submit.prevent="createComment(props.article.id)"
      class="comment-form"
    >
      <h3 class="comment-title">댓글 작성</h3>
      <label for="content" class="content-label"></label>
      <textarea
        id="content"
        v-model.trim="content"
        class="comment-input"
        placeholder="댓글을 입력하세요..."
      ></textarea>
      <button type="submit" class="submit-btn">제출</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import ArticleCommentListItem from "./ArticleCommentListItem.vue";
import axios from "axios";

const store = useCounterStore();
const content = ref("");

const props = defineProps({
  article: Object,
});

onMounted(async () => {
  store.getArticleComments(props.article.id);
});

const createComment = function (article_id) {
  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/articles/${article_id}/comments/`,
    data: {
      content: content.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      content.value = "";
      store.getArticleComments(article_id);
    })
    .catch((err) => {
      if (err.response.data.error) {
        alert(err.response.data.error);
      }
    });
};
</script>

<style scoped>
.comment-section {
  padding: 20px;
  background-color: #121212; /* 어두운 배경 */
  color: white;
}

.comment-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #f56565; /* 빨간색 제목 */
  margin-bottom: 10px;
}

.content-label {
  font-size: 0.875rem;
  color: #cbd5e0; /* 밝은 회색 */
  margin-bottom: 8px;
  display: block;
}

.comment-input {
  width: 100%;
  height: 120px;
  padding: 10px;
  background-color: #2d3748; /* 어두운 회색 배경 */
  color: #e2e8f0; /* 밝은 회색 글자 */
  border: 1px solid #444;
  border-radius: 8px;
  resize: none;
  font-size: 1rem;
  margin-bottom: 12px;
}

.comment-input::placeholder {
  color: #aaa; /* 댓글 입력란 placeholder 색상 */
}

.submit-btn {
  background-color: #f56565;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s, transform 0.3s;
}

.submit-btn:hover {
  background-color: #c53030;
  transform: scale(1.05);
}

.comment-list {
  margin-top: 20px;
}

.no-comments {
  color: #cbd5e0;
  text-align: center;
}

@media (max-width: 768px) {
  .comment-input {
    height: 100px;
    font-size: 0.875rem;
  }

  .submit-btn {
    padding: 8px 16px;
    font-size: 0.875rem;
  }
}
</style>
