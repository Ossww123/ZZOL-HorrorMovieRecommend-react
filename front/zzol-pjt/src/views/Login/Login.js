import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // useHistory -> useNavigate
import { loginUser } from "../../api/auth"; // 로그인 API 요청을 위한 함수

function Login() {
  const [username, setUsername] = useState(""); // 사용자 이름 상태
  const [password, setPassword] = useState(""); // 비밀번호 상태
  const [isSubmitting, setIsSubmitting] = useState(false); // 로딩 상태
  const navigate = useNavigate(); // 리디렉션을 위한 navigate 객체

  // 로그인 처리 함수
  const logInHandler = async (e) => {
    e.preventDefault(); // 기본 폼 제출 방지

    const payload = {
      username,
      password,
    };

    setIsSubmitting(true);

    try {
      const response = await loginUser(payload); // 로그인 API 호출
      localStorage.setItem("token", response.key); // 로그인 성공 시 토큰 저장

      // 홈 페이지로 리디렉션
      navigate("/"); // history.push -> navigate
    } catch (error) {
      console.error("Login failed:", error.response ? error.response.data : error);
    } finally {
      setIsSubmitting(false); // 제출 후 로딩 상태 해제
    }
  };

  return (
    <div className="login-container">
      <h1 className="text-2xl font-bold">LogIn</h1>
      <form onSubmit={logInHandler}>
        {/* Username */}
        <div>
          <label htmlFor="username">Username: </label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)} // 입력값 관리
          />
        </div>

        {/* Password */}
        <div>
          <label htmlFor="password">Password: </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // 입력값 관리
          />
        </div>

        {/* Submit Button */}
        <button type="submit" disabled={isSubmitting}>
          Log In
        </button>

        {/* 로딩 스피너 */}
        {isSubmitting && <div className="spinner">Loading...</div>}
      </form>
    </div>
  );
}

export default Login;
