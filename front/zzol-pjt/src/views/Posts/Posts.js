// src/views/Posts/Posts.js

import React, { useState, useEffect, useCallback } from "react";
import { getArticles } from "../../api/post"; // API 호출 함수 import
import { useAuth } from "../../context/AuthContext"; // AuthContext import
import { useNavigate } from "react-router-dom"; // 페이지 이동을 위한 useNavigate import

const Posts = () => {
  const { token } = useAuth(); // AuthContext에서 token 가져오기
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // 페이지 이동을 위한 navigate 사용

  // 게시글 목록을 가져오는 함수
  const fetchArticles = useCallback(async () => {
    setLoading(true);
    setError(null); // 에러 상태 초기화
    try {
      const data = await getArticles(token); // getArticles API 호출
      setArticles(data); // 응답 받은 게시글 데이터를 상태에 저장
    } catch (err) {
      setError("게시글을 불러오는 데 실패했습니다."); // 에러 메시지 설정
      console.error(err);
    } finally {
      setLoading(false); // 로딩 상태 false로 설정
    }
  }, [token]);

  // 컴포넌트가 처음 렌더링될 때 게시글을 요청
  useEffect(() => {
    if (token) {
      fetchArticles(); // 토큰이 있을 경우에만 API 호출
    }
  }, [token, fetchArticles]); // token이 변경될 때마다 다시 호출

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner">Loading...</div>{" "}
        {/* 스피너나 로딩 애니메이션 */}
      </div>
    );
  }

  if (error) {
    return <div className="error-message">{error}</div>; // 에러 메시지 표시
  }

  const handleViewMore = (id) => {
    navigate(`/articles/${id}`); // 클릭 시 상세 페이지로 이동
  };

  const handleCreatePost = () => {
    navigate(`/articles/new`); // 게시글 생성 페이지로 이동
  };

  return (
    <div className="posts-container">
      <h1>게시글 목록</h1>
      <button onClick={handleCreatePost} className="create-post-btn">
        게시글 생성
      </button> {/* 게시글 생성 버튼 */}
      <ul className="posts-list">
        {articles.remaining_articles.map((article) => (
          <li key={article.id} className="post-item">
            <h3>{article.title}</h3>
            <p>{article.content.slice(0, 100)}...</p> {/* 내용 일부만 표시 */}
            <button
              onClick={() => handleViewMore(article.id)}
              className="view-more-btn"
            >
              더 보기
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Posts;
