import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createArticle } from "../../api/post";
import { useAuth } from "../../context/AuthContext";

const CreateArticle = () => {
  const { token } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    title: "",
    content: "",
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.title) newErrors.title = "제목을 입력하세요.";
    if (!formData.content) newErrors.content = "내용을 입력하세요.";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      await createArticle(token, formData);
      navigate("/articles"); // 게시글 목록 페이지로 이동
    } catch (error) {
      console.error(error);
      setErrors({ general: "게시글 생성에 실패했습니다." });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="create-article-container">
      <h1>새로운 게시글 작성</h1>
      <form onSubmit={handleSubmit}>
        {errors.general && <p className="error">{errors.general}</p>}
        <div>
          <label htmlFor="title">제목:</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className={errors.title ? "input-error" : ""}
          />
          {errors.title && <p className="error">{errors.title}</p>}
        </div>
        <div>
          <label htmlFor="content">내용:</label>
          <textarea
            id="content"
            name="content"
            value={formData.content}
            onChange={handleChange}
            className={errors.content ? "input-error" : ""}
          />
          {errors.content && <p className="error">{errors.content}</p>}
        </div>
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "작성 중..." : "작성하기"}
        </button>
      </form>
    </div>
  );
};

export default CreateArticle;
