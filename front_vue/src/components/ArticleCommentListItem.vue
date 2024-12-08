<template>
  <div class="comment-item">
    <div v-if="!isEditing" class="comment-body">
      <div class="comment-header">
        <h5 class="comment-author">{{ props.comment.user.nickname }}</h5>
        <span class="comment-date">{{
          formatDate(props.comment.created_at)
        }}</span>
      </div>
      <p class="comment-content">{{ props.comment.content }}</p>
      <div class="comment-actions">
        <button @click="startEdit" class="edit-btn">수정</button>
        <button
          @click="deleteComment(props.article_pk, props.comment.id)"
          class="delete-btn"
        >
          삭제
        </button>
      </div>
    </div>

    <!-- 수정 상태 -->
    <div v-else class="edit-body">
      <textarea v-model="editedContent" class="edit-input"></textarea>
      <div class="edit-actions">
        <button
          @click="updateComment(props.article_pk, props.comment.id)"
          class="save-btn"
        >
          저장
        </button>
        <button @click="cancelEdit" class="cancel-btn">취소</button>
      </div>
    </div>
    <hr />
  </div>
</template>

<script setup>
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { ref } from "vue";

const store = useCounterStore();
const editedContent = ref("");
const isEditing = ref(false);

const props = defineProps({
  article_pk: String,
  comment: Object,
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("ko-KR"); // 날짜 포맷
};

const deleteComment = function (article_pk, comment_Id) {
  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/articles/${article_pk}/comments/${comment_Id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      store.getArticleComments(article_pk);
    })
    .catch((err) => {
      console.log("댓글 삭제 실패", err);
    });
};

const startEdit = () => {
  editedContent.value = props.comment.content;
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
  editedContent.value = "";
};

const updateComment = function (article_pk, comment_Id) {
  axios({
    method: "put",
    url: `${store.API_URL}/api/v1/articles/${article_pk}/comments/${comment_Id}/`,
    data: {
      content: editedContent.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      store.getArticleComments(props.article_pk);
      isEditing.value = false;
    })
    .catch((err) => {
      console.log("댓글 수정 실패", err);
    });
};
</script>

<style scoped>
.comment-item {
  padding: 15px;
  background-color: #1a202c; /* 어두운 배경 */
  border-radius: 8px;
  margin-bottom: 15px;
  color: white;
}

.comment-body {
  display: flex;
  flex-direction: column;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: bold;
  color: #e53e3e; /* 빨간색 텍스트 */
}

.comment-date {
  color: #a0aec0; /* 밝은 회색 텍스트 */
}

.comment-content {
  margin-bottom: 12px;
  color: #e2e8f0; /* 밝은 회색 */
}

.comment-actions {
  display: flex;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  padding: 6px 12px;
  background-color: #f56565;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.edit-btn:hover,
.delete-btn:hover {
  background-color: #c53030;
  transform: scale(1.05);
}

.delete-btn {
  background-color: #e53e3e; /* 삭제 버튼 빨간색 */
}

.edit-body {
  display: flex;
  flex-direction: column;
}

.edit-input {
  padding: 10px;
  background-color: #2d3748;
  color: #e2e8f0;
  border: 1px solid #444;
  border-radius: 8px;
  margin-bottom: 10px;
  font-size: 1rem;
  resize: none;
}

.edit-actions {
  display: flex;
  gap: 15px;
}

.save-btn,
.cancel-btn {
  padding: 8px 16px;
  background-color: #f56565;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.save-btn:hover,
.cancel-btn:hover {
  background-color: #c53030;
  transform: scale(1.05);
}

.cancel-btn {
  background-color: #4a5568; /* 취소 버튼 색상 */
}

hr {
  border: 1px solid #2d3748;
  margin: 10px 0;
}
</style>
