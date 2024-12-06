// src/views/Home/Home.js

import React from "react";
import { useAuth } from "../../context/AuthContext"; // AuthContext를 통해 로그인 상태 확인

const Home = () => {
  const { token, logout } = useAuth(); // token과 logout 함수 가져오기

  return (
    <div className="home-container">
      <h1>환영합니다!</h1>
      {token ? (
        <div>
          <p>로그인하신 사용자입니다.</p>
          <button onClick={logout}>로그아웃</button>
        </div>
      ) : (
        <p>로그인 상태가 아닙니다. 로그인 후 이용하세요.</p>
      )}
    </div>
  );
};

export default Home;
