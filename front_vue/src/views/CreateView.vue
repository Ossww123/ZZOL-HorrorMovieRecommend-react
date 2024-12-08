<template>
  <div
    class="min-h-screen bg-black flex items-center justify-center py-12 px-4"
  >
    <div
      class="w-full max-w-xl bg-[#1a1a1a] border border-red-900/30 rounded-xl shadow-2xl shadow-red-900/20 p-8"
    >
      <h1
        class="text-4xl font-bold text-red-600 text-center mb-8 tracking-wider drop-shadow-[0_0_10px_rgba(220,38,38,0.5)]"
      >
        게시글 작성
      </h1>

      <form @submit.prevent="createArticle">
        <div class="mb-6">
          <label for="title" class="block text-lg mb-2 text-gray-300">
            제목
          </label>
          <input
            type="text"
            id="title"
            v-model.trim="title"
            required
            placeholder="제목을 입력하세요"
            class="w-full p-3 rounded-lg bg-black/40 text-white border border-red-900/30 focus:outline-none focus:ring-2 focus:ring-red-600 transition-all duration-300 placeholder-gray-500"
          />
        </div>

        <div class="mb-8">
          <label for="content" class="block text-lg mb-2 text-gray-300">
            내용
          </label>
          <textarea
            id="content"
            v-model.trim="content"
            required
            rows="10"
            placeholder="여기에 내용을 작성하세요..."
            class="w-full p-3 rounded-lg bg-black/40 text-white border border-red-900/30 focus:outline-none focus:ring-2 focus:ring-red-600 transition-all duration-300 placeholder-gray-500 resize-none"
          ></textarea>
        </div>

        <div class="flex flex-col space-y-4">
          <button
            type="submit"
            class="w-full py-3 bg-red-900/50 text-white font-bold rounded-lg shadow-lg hover:bg-red-900/70 transition-all duration-300 ease-in-out transform hover:scale-[1.02] active:scale-[0.98]"
          >
            게시글 작성
          </button>

          <button
            type="button"
            @click="cancelWrite"
            class="w-full py-3 bg-gray-800 text-gray-400 rounded-lg hover:bg-gray-700 transition-all duration-300"
          >
            취소
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { useRouter } from "vue-router";

const title = ref("");
const content = ref("");
const store = useCounterStore();
const router = useRouter();

const createArticle = async () => {
  try {
    // 제목과 내용 유효성 검사 추가
    if (!title.value.trim()) {
      alert("제목을 입력해주세요.");
      return;
    }

    if (!content.value.trim()) {
      alert("내용을 입력해주세요.");
      return;
    }

    const response = await axios.post(
      `${store.API_URL}/api/v1/articles/`,
      {
        title: title.value,
        content: content.value,
      },
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    // 게시글 작성 성공 알림
    alert("게시글이 성공적으로 작성되었습니다.");

    // 게시글 상세 페이지 또는 목록 페이지로 이동
    router.push({
      name: "ArticleDetail",
      params: { id: response.data.id },
    });
  } catch (error) {
    console.error(error);
    alert("게시글 작성 중 오류가 발생했습니다.");
  }
};

const cancelWrite = () => {
  // 작성 취소 시 확인 모달
  const confirmed = confirm(
    "작성 중인 내용이 삭제됩니다. 정말 취소하시겠습니까?"
  );
  if (confirmed) {
    router.push({ name: "ArticleView" });
  }
};
</script>

<style scoped>
/* 추가 스타일링 */
input,
textarea {
  transition: all 0.3s ease;
}

input:focus,
textarea:focus {
  box-shadow: 0 0 15px rgba(220, 38, 38, 0.3);
}
</style>
