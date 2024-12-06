// src/components/Navbar/Navbar.js

import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext"; // AuthContext import

function Navbar() {
  const { token, logout } = useAuth(); // AuthContext에서 token과 logout 함수 가져오기
  const [searchQuery, setSearchQuery] = useState(""); // 검색어 상태
  const navigate = useNavigate(); // 리디렉션을 위한 useNavigate 훅

  // 검색 처리 함수
  const handleSearch = () => {
    if (searchQuery) {
      navigate({
        pathname: "/movies",
        search: `?search=${searchQuery}`,
      });
    }
  };

  // 로그아웃 함수
  const handleLogout = () => {
    logout(); // Context의 logout 함수 호출
  };

  // `token`이 변경되었을 때 navbar가 다시 렌더링되도록 useEffect 사용
  useEffect(() => {
    // 필요 시 token에 의한 추가 작업을 할 수 있습니다.
  }, [token]);

  return (
    <nav className="bg-black text-white p-4 flex items-center">
      <Link to="/" className="mr-4">
        {/* 실제 로고 경로로 수정하세요 */}
        <img src="/logo.png" alt="Logo" className="h-16" />
      </Link>

      <div className="flex space-x-6">
        <Link to="/" className="hover:text-gray-400">Home</Link>
        <Link to="/articles" className="hover:text-gray-400">Articles</Link>
        <Link to="/movies" className="hover:text-gray-400">Movies</Link>
      </div>

      <div className="ml-auto flex items-center space-x-4">
        {!token ? (
          <>
            <Link to="/login" className="hover:text-gray-400">로그인</Link>
            <Link to="/signup" className="hover:text-gray-400">회원가입</Link>
          </>
        ) : (
          <>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)} // 입력값 상태 업데이트
              placeholder="영화 제목 검색"
              className="p-2"
            />
            <button onClick={handleSearch} className="p-2 hover:text-gray-400">검색</button>
            <button onClick={handleLogout} className="hover:text-gray-400">로그아웃</button>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
