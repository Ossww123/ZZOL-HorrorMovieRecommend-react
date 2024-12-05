import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom"; // useHistory -> useNavigate

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // 로그인 상태
  const [searchQuery, setSearchQuery] = useState(""); // 검색어 상태
  const navigate = useNavigate(); // 리디렉션을 위한 useNavigate 훅

  // 로그인 상태 체크 (로컬 스토리지에서 토큰을 확인)
  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token); // 토큰이 있으면 로그인 상태로 설정
  }, []);

  // 검색 처리 함수 (디바운스 없이 간단히 구현)
  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    if (e.target.value) {
      navigate({
        pathname: "/movies",
        search: `?search=${e.target.value}`, // 검색 쿼리 파라미터 추가
      });
    }
  };

  // 로그아웃 함수
  const handleLogout = () => {
    localStorage.removeItem("token"); // 토큰 제거하여 로그아웃 처리
    setIsLoggedIn(false); // 로그인 상태 업데이트
  };

  return (
    <nav className="bg-black text-white p-4 flex items-center">
      {/* 로고 */}
      <Link to="/" className="mr-4">
        <img src="/path/to/logo.png" alt="Logo" className="h-16" />
      </Link>

      {/* 네비게이션 링크들 왼쪽 정렬 */}
      <div className="flex space-x-6">
        <Link to="/" className="hover:text-gray-400">
          Home
        </Link>
        <Link to="/articles" className="hover:text-gray-400">
          Articles
        </Link>
        <Link to="/movies" className="hover:text-gray-400">
          Movies
        </Link>
      </div>

      {/* 로그인 상태에 따른 버튼 표시 */}
      <div className="ml-auto flex items-center space-x-4">
        {!isLoggedIn ? (
          <>
            {/* 로그인, 회원가입 버튼들 */}
            <Link to="/login" className="hover:text-gray-400">
              로그인
            </Link>
            <Link to="/signup" className="hover:text-gray-400">
              회원가입
            </Link>
          </>
        ) : (
          <>
            {/* 검색 창 */}
            <input
              type="text"
              value={searchQuery}
              onChange={handleSearch}
              placeholder="영화 제목 검색"
              className="p-2"
            />
            {/* 로그아웃 버튼 */}
            <button onClick={handleLogout} className="hover:text-gray-400">
              로그아웃
            </button>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
