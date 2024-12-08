import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getArticleDetail } from "../../api/post";
import { useAuth } from "../../context/AuthContext";

const ArticleDetail = () => {
  const { id } = useParams();
  const { token } = useAuth();
  const [article, setArticle] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const data = await getArticleDetail(token, id);
        setArticle(data);
      } catch (err) {
        console.error(err);
        setError("게시글을 불러오는 데 실패했습니다.");
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [id, token]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="article-detail-container">
      <h1>{article.title}</h1>
      <p>{article.content}</p>
    </div>
  );
};

export default ArticleDetail;
