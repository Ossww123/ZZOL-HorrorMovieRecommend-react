// src/views/SignUp/SignUp.js

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signUpUser, loginUser } from "../../api/auth";
import { useAuth } from "../../context/AuthContext"; // AuthContext import

const InputField = ({ label, name, value, onChange, error, type = "text" }) => (
  <div className="input-field">
    <label htmlFor={name}>{label}:</label>
    <input
      type={type}
      id={name}
      name={name}
      value={value}
      onChange={onChange}
      className="input"
    />
    {error && <p className="error">{error}</p>}
  </div>
);

// 이메일 유효성 검사
const isValidEmail = (email) => {
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(email);
};

// 비밀번호 확인
const passwordsMatch = (password1, password2) => password1 === password2;

function SignUp() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password1: "",
    password2: "",
    nickname: "",
    profileimage: null, // 이미지 파일 초기화
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [imagePreview, setImagePreview] = useState(null); // 이미지 미리보기 상태 추가
  const navigate = useNavigate();
  const { login } = useAuth(); // 로그인 함수 가져오기

  const validateForm = () => {
    const newErrors = {};
    let valid = true;
    if (!formData.username) {
      newErrors.username = "Username을 입력하세요.";
      valid = false;
    }
    if (!formData.email) {
      newErrors.email = "Email을 입력하세요.";
      valid = false;
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = "잘못된 이메일 형식입니다.";
      valid = false;
    }
    if (!formData.password1) {
      newErrors.password1 = "Password를 입력하세요.";
      valid = false;
    }
    if (!formData.password2) {
      newErrors.password2 = "Password confirmation을 입력하세요.";
      valid = false;
    } else if (!passwordsMatch(formData.password1, formData.password2)) {
      newErrors.password2 = "비밀번호가 일치하지 않습니다.";
      valid = false;
    }
    if (!formData.nickname) {
      newErrors.nickname = "Nickname을 입력하세요.";
      valid = false;
    }
    setErrors(newErrors);
    return valid;
  };

  const handleChange = (e) => {
    if (e.target.name === "profileimage") {
      const file = e.target.files[0];
      setFormData((prev) => ({
        ...prev,
        profileimage: file,
      }));

      // 이미지 미리보기 설정
      if (file) {
        const previewUrl = URL.createObjectURL(file);
        setImagePreview(previewUrl);
      }
    } else {
      setFormData((prev) => ({
        ...prev,
        [e.target.name]: e.target.value,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      // FormData 객체를 생성하여 이미지와 다른 데이터 함께 전송
      const formDataToSubmit = new FormData();
      formDataToSubmit.append("username", formData.username);
      formDataToSubmit.append("email", formData.email);
      formDataToSubmit.append("password", formData.password1);
      formDataToSubmit.append("nickname", formData.nickname);

      // 이미지 파일이 있을 경우 추가
      if (formData.profileimage) {
        formDataToSubmit.append("profileimage", formData.profileimage);
      }

      // 회원가입 API 호출
      await signUpUser(formDataToSubmit);

      // 로그인
      const loginResponse = await loginUser({
        username: formData.username,
        password: formData.password1,
      });
      login(loginResponse.key); // 회원가입 후 로그인 처리
      navigate("/"); // 홈 페이지로 리디렉션
    } catch (error) {
      console.error(
        "Signup failed:",
        error.response ? error.response.data : error
      );
      setErrors({ general: "회원가입에 실패했습니다. 다시 시도해 주세요." });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="signup-container">
      <h1>회원가입</h1>
      <form onSubmit={handleSubmit}>
        {errors.general && <p className="error">{errors.general}</p>}
        <InputField
          label="Username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          error={errors.username}
        />
        <InputField
          label="Email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          type="email"
        />
        <InputField
          label="Password"
          name="password1"
          value={formData.password1}
          onChange={handleChange}
          error={errors.password1}
          type="password"
        />
        <InputField
          label="Confirm Password"
          name="password2"
          value={formData.password2}
          onChange={handleChange}
          error={errors.password2}
          type="password"
        />
        <InputField
          label="Nickname"
          name="nickname"
          value={formData.nickname}
          onChange={handleChange}
          error={errors.nickname}
        />

        {/* Profile image upload field */}
        <div className="image-upload">
          <label htmlFor="profileimage">Profile Image:</label>
          <input
            type="file"
            id="profileimage"
            name="profileimage"
            onChange={handleChange}
          />
          {imagePreview && (
            <img src={imagePreview} alt="Preview" className="image-preview" />
          )}
        </div>

        <button type="submit" disabled={isSubmitting} className="submit-btn">
          {isSubmitting ? "가입 중..." : "회원가입"}
        </button>
      </form>
    </div>
  );
}

export default SignUp;
