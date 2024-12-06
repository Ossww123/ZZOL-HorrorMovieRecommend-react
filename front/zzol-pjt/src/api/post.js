// src/api/post.js
import axios from 'axios';

// API 기본 URL
const API_URL = "http://127.0.0.1:8000/api/v1";

// 게시글 목록을 가져오는 함수
export const getArticles = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/articles/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    return response.data; // 서버에서 받은 게시글 데이터를 반환
  } catch (error) {
    console.error("Error fetching articles:", error.response || error);
    throw error; // 오류 발생 시 예외를 던짐
  }
};
