// App.js

import "./App.css";
import React from "react";
import Navbar from "./components/Navbar/Navbar";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom"; // Navigate 추가
import Login from "./views/Login/Login";
import SignUp from "./views/SignUp/SignUp";
import Home from "./views/Home/Home"; // Home 컴포넌트 추가
import { AuthProvider, useAuth } from "./context/AuthContext"; // AuthContext 가져오기
import Posts from "./views/Posts/Posts";

// 로그인 또는 회원가입 페이지에 접근하려고 할 때, 이미 로그인된 상태라면 리디렉션 처리
const ProtectedRoute = ({ element }) => {
  const { token } = useAuth();
  return token ? <Navigate to="/" /> : element; // 로그인 상태면 홈으로 리디렉션
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} /> {/* 홈 페이지 추가 */}
          <Route
            path="/login"
            element={<ProtectedRoute element={<Login />} />} // 로그인 페이지 접근 보호
          />
          <Route
            path="/signup"
            element={<ProtectedRoute element={<SignUp />} />} // 회원가입 페이지 접근 보호
          />
          <Route path="/articles" element={<Posts />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
