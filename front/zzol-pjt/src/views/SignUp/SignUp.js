import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // useHistory -> useNavigate
import { signUpUser, loginUser } from "../../api/auth";

// 재사용 가능한 입력 필드 컴포넌트
const InputField = ({ label, name, value, onChange, error, type = "text" }) => (
  <div>
    <label htmlFor={name}>{label}:</label>
    <input
      type={type}
      id={name}
      name={name}
      value={value}
      onChange={onChange}
    />
    {error && <p>{error}</p>}
  </div>
);

function SignUp() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password1: "",
    password2: "",
    nickname: "",
    profileimage: null,
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate(); // 리디렉션을 위한 navigate 객체

  // 이메일 형식 검증
  const isValidEmail = (email) =>
    /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);

  // 비밀번호 일치 여부 체크
  const passwordsMatch = (password1, password2) => password1 === password2;

  // 이미지 업로드 핸들러
  const handleImageUpload = (e) => {
    setFormData({ ...formData, profileimage: e.target.files[0] });
  };

  // 폼 검증
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

  // 회원가입 핸들러
  const signUpHandler = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsSubmitting(true);

    const formDataToSend = new FormData();
    Object.keys(formData).forEach((key) =>
      formDataToSend.append(key, formData[key])
    );

    try {
      await signUpUser(formDataToSend);

      const loginData = {
        username: formData.username,
        password: formData.password1,
      };
      const loginResponse = await loginUser(loginData);

      localStorage.setItem("token", loginResponse.key);
      navigate("/"); // history.push -> navigate
    } catch (error) {
      console.error(
        "Error during sign up:",
        error.response ? error.response.data : error
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  // 입력값 변경 처리
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div>
      <h1>Sign Up Page</h1>

      <form onSubmit={signUpHandler}>
        <InputField
          label="Username"
          name="username"
          value={formData.username}
          onChange={handleInputChange}
          error={errors.username}
        />
        <InputField
          label="Email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          error={errors.email}
        />
        <InputField
          label="Password"
          name="password1"
          value={formData.password1}
          onChange={handleInputChange}
          error={errors.password1}
          type="password"
        />
        <InputField
          label="Password Confirmation"
          name="password2"
          value={formData.password2}
          onChange={handleInputChange}
          error={errors.password2}
          type="password"
        />
        <InputField
          label="Nickname"
          name="nickname"
          value={formData.nickname}
          onChange={handleInputChange}
          error={errors.nickname}
        />

        <div>
          <label htmlFor="profileimage">Profile Image:</label>
          <input type="file" id="profileimage" onChange={handleImageUpload} />
          {errors.profileimage && <p>{errors.profileimage}</p>}
        </div>

        <button type="submit" disabled={isSubmitting}>
          Sign Up
        </button>

        {isSubmitting && <div>Loading...</div>}
      </form>
    </div>
  );
}

export default SignUp;
