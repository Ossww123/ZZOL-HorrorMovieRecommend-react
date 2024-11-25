// stores/counter.js

import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const movies = ref([])
  const movieDetail = ref([])
  const randomDetail = ref([])
  const popularMovies = ref([])
  const latestMovies = ref([])
  const ratingMovies = ref([])
  const randomReviews = ref([])
  const fearMovies = ref([])
  const reviews = ref([])
  const comments = ref([])
  const articleComments = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const profileImage = ref(""); // 프로필 이미지 상태 추가
  const nickname = ref("");
  const email = ref("");
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

    // 유저 정보 요청 후 프로필 사진 저장
    const fetchUserProfile = () => {
      axios({
        method: "get",
        url: `${API_URL}/accounts/user/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((response) => {
          console.log("Profile response:", response.data); // 서버 응답 확인
          profileImage.value = response.data.profileimage || ""; // profile_image 값 설정
          nickname.value = response.data.nickname || "닉네임 없음";
          email.value = response.data.email || "이메일 없음";
          console.log("Updated profile image:", profileImage.value); // 갱신된 값 확인
        })
        .catch((err) => {
          console.log("프로필 정보 가져오기 실패", err);
        });
    };

    // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          console.log(res.data);
          articles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };


    // 리뷰에 대한 댓글 가져와서 comments에 저장하는 함수
    const getReviewComments = function (review_pk) {
      axios
        .get(`${API_URL}/api/v1/${review_pk}/comments/`, {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })
        .then((res) => {
          console.log("여기 댓글 있어요");
          console.log(res.data);
          comments.value = res.data;
          console.log(comments.value);
        })
        .catch((err) => {
          console.log("댓글 에러");
          console.log(err);
        });
    };

    const getArticleComments = function (article_pk) {
      axios
        .get(`${API_URL}/api/v1/articles/${article_pk}/comments/`, {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })
        .then((res) => {
          console.log("여기 댓글 있어요");
          console.log(res.data);
          articleComments.value = res.data;
          console.log(articleComments.value);
        })
        .catch((err) => {
          console.log("댓글 에러");
          console.log(err);
        });
    };

    // 영화 정보 가져와서 movies에 저장하는 함수
    const getMovies = () => {
      // axios 는 Promise 객체와 동일하게 활용한다.
      axios
        .get(`${API_URL}/api/v1/movies/`, {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })
        .then((response) => {
          console.log(response.data);
          // console.log('Movies fetched = ', response.data);
          movies.value = response.data;
        })
        .catch((error) => {
          console.log("error = ", error);
        });
    };

    const getMovieDetail = (movie_pk) => {
      // axios 는 Promise 객체와 동일하게 활용한다.
      axios
        .get(`${API_URL}/api/v1/movies/${movie_pk}/`, {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })
        .then((response) => {
          console.log(response.data);
          // console.log('Movies fetched = ', response.data);
          movieDetail.value = response.data;
          console.log(movieDetail.value);
        })
        .catch((error) => {
          console.log("error = ", error);
        });
    };


  const getMovieReviews = async function (movie_pk) {
      const response = await axios.get(`${API_URL}/api/v1/${movie_pk}/reviews/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      reviews.value = response.data
      return response.data
  }

  const getRandomMovieReviews = function (tmdb_id) {
    axios.get(`${API_URL}/api/v1/random/${tmdb_id}/reviews/`, {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res) => {
      console.log("이까지오나")
      console.log(res.data)
      randomReviews.value = res.data
      console.log(randomReviews.value)
    })
    .catch((err) => {
      console.log("아님여긴가")
      console.log(err)
    })
  }

    // 랜덤 영화
    const getRandomMovies = async () => {
      const response = await axios.get(`${API_URL}/api/v1/random/`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      return response.data;
    };

    // 회원가입 요청 액션
    const signUp = function (payload) {
      // const username = payload.username
      // const password1 = payload.password1
      // const password2 = payload.password2
      const { username, email, password1, password2, nickname } = payload;
      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          email,
          password1,
          password2,
          nickname,
        },
      })
    }
      

  const getMovieList = async (sortBy) => {
    const response = await axios.get(`${API_URL}/api/v1/movielist/`, {
      params: { sort: sortBy },
      headers: {
        Authorization: `Token ${token.value}`,
      },
      
    })
    switch(sortBy) {
      case 'popularity':
        popularMovies.value = response.data;
        break;
      case 'latest':
        latestMovies.value = response.data;
        break;
      case 'rating':
        ratingMovies.value = response.data;
        break;
      case 'fear':
        fearMovies.value = response.data;
        break;
    }
  }

  const getRandomDetail = async (movieId) => {
    try {
      const response = await axios.get(
        `${API_URL}/api/v1/random/${movieId}/`,
        {
          headers: {
            Authorization: `Token ${token.value}`
          }
        }
      )
      randomDetail.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching movie:', error)
      throw error
    }
  }


    // 로그인 요청 액션
    const logIn = function (payload) {
      // const username = payload.username
      // const password1 = payload.password
      const { username, password } = payload;

      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          token.value = res.data.key;
          fetchUserProfile(); // 로그인 후 유저 프로필 이미지 가져오기
          router.push({ name: "ArticleView" });
          // console.log(res.data)
          // console.log('로그인 성공')
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // [추가기능] 로그아웃 by 준호
    const logOut = function () {
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
      })
        .then((res) => {
          console.log(res.data);
          token.value = null;
          profileImage.value = ""; // 로그아웃 시 프로필 이미지 초기화
          router.push({ name: "ArticleView" });
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 여러 개의 컴포넌트에서 활용하는 데이터만
    // store 로 관리해야 한다!
    // -> 여러 명이 작업할 때 체감이 될 것!
    let carts = ref([]);

    const apiKey = import.meta.env.VITE_TMDB;

    // 데이터 다운로드

    // 상세 페이지 상품 조회
    const getMovieById = (id) => {
      const movie = movies.value.find((movie) => movie.id == id);
      console.log("movie = ", movie);
      return movie;
    };


  return { articles, API_URL, reviews, comments, popularMovies, latestMovies, ratingMovies, fearMovies, randomDetail, randomReviews, articleComments, getArticleComments, getRandomMovieReviews, getRandomDetail, getRandomMovies, getMovieList, getReviewComments, getArticles, getMovieReviews, signUp, logIn, token, isLogin, logOut, movies, carts, getMovies, getMovieById, getMovieDetail, movieDetail, fetchUserProfile,
      profileImage,
      nickname,
      email,  }
}, { persist: true })

