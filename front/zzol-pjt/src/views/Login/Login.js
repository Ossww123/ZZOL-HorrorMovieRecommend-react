// src/views/Login/Login.js

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../../api/auth";
import { useAuth } from "../../context/AuthContext"; // AuthContext import

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({}); // 에러 메시지 상태 추가
  const navigate = useNavigate();
  const { login } = useAuth(); // 로그인 함수 가져오기

  // 입력값 검증 함수
  const validateForm = () => {
    const newErrors = {};
    let isValid = true;

    if (!username) {
      newErrors.username = "Username을 입력하세요.";
      isValid = false;
    }
    if (!password) {
      newErrors.password = "Password을 입력하세요.";
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const logInHandler = async (e) => {
    e.preventDefault();

    // 입력값 검증
    if (!validateForm()) return;

    const payload = {
      username,
      password,
    };

    setIsSubmitting(true);

    try {
      const response = await loginUser(payload);
      login(response.key); // 로그인 후 token을 AuthContext에 저장
      navigate("/"); // 홈 페이지로 리디렉션
    } catch (error) {
      console.error("Login failed:", error.response ? error.response.data : error);
      setErrors({ general: "로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요." }); // 에러 메시지 설정
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-container">
      <h1 className="text-2xl font-bold">LogIn</h1>
      <form onSubmit={logInHandler}>
        <div>
          <label htmlFor="username">Username: </label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className={errors.username ? "input-error" : ""}
          />
          {errors.username && <p className="text-red-500">{errors.username}</p>} {/* 에러 메시지 표시 */}
        </div>

        <div>
          <label htmlFor="password">Password: </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={errors.password ? "input-error" : ""}
          />
          {errors.password && <p className="text-red-500">{errors.password}</p>} {/* 에러 메시지 표시 */}
        </div>

        {errors.general && <p className="text-red-500">{errors.general}</p>} {/* 로그인 실패 메시지 */}

        <button type="submit" disabled={isSubmitting} className="btn-login">
          {isSubmitting ? "로그인 중..." : "Log In"}
        </button>

        {isSubmitting && <div className="spinner">Loading...</div>}
      </form>
    </div>
  );
}

export default Login;
