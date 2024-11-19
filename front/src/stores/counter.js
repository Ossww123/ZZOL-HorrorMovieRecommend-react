import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 회원가입 요청 액션
  const signUp = function (payload) {
    // const username = payload.username
    // const password1 = payload.password1
    // const password2 = payload.password2
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        // console.log(res)
        // console.log('회원가입 성공')
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    // const username = payload.username
    // const password1 = payload.password
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.key
        router.push({ name: 'ArticleView' })
        // console.log(res.data)
        // console.log('로그인 성공')
      })
      .catch((err) => {
        console.log(err)
      })
  }
  
  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }


  // 여러 개의 컴포넌트에서 활용하는 데이터만
  // store 로 관리해야 한다!
  // -> 여러 명이 작업할 때 체감이 될 것!
  let movies = ref([]);
  let carts = ref([]);

  const apiKey = import.meta.env.VITE_TMDB;

  // 데이터 다운로드
  const getMovies = () => {
    // axios 는 Promise 객체와 동일하게 활용한다.
    axios.get(`https://api.themoviedb.org/3/movie/top_rated?api_key=${apiKey}&language=ko-KR&page=1`)
    .then((response) => {
      console.log('response = ', response);
      console.log('Movies fetched = ', response.data);
      movies.value = response.data.results;
    }).catch((error) => {
      console.log("error = ", error);
    })
  }

  // 상세 페이지 상품 조회
  const getMovieById = (id) => {
    const movie = movies.value.find((movie) => movie.id == id)
    console.log("movie = ", movie)
    return movie
  }

  return { articles, API_URL, getArticles, signUp, logIn, token, isLogin, logOut, movies, carts, getMovies, getMovieById  }
}, { persist: true })
