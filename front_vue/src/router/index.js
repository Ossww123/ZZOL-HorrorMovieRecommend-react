// router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import { useCounterStore } from '@/stores/counter'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieListView from '@/views/MovieListView.vue'
import ReviewSearchView from '@/views/ReviewSearchView.vue'
import RecommendedView from '@/views/RecommendedView.vue'
import HomeView from '@/views/HomeView.vue'
import RandomTestView from '@/views/RandomTestView.vue'
import RandomMovieDetailView from '@/views/RandomMovieDetailView.vue'
import ProfileView from "@/views/ProfileView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomeView",
      component: HomeView,
    },
    {
      path: "/articles",
      name: "ArticleView",
      component: ArticleView,
    },
    {
      path: "/articles/:id",
      name: "DetailView",
      component: DetailView,
    },
    {
      path: "/create",
      name: "CreateView",
      component: CreateView,
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/movies",
      name: "MovieListView",
      component: MovieListView,
    },
    {
      path: "/:movie_id",
      name: "MovieDetailView",
      component: MovieDetailView,
    },
    {
      path: "/review-search",
      component: ReviewSearchView,
    },
    {
      path: "/recommended",
      component: RecommendedView,
    },
    {
      path: "/random",
      component: RandomTestView,
    },
    {
      path: "/profile",
      name: "ProfileView",
      component: ProfileView,
    },

    {
      path: '/random/:movie_id',
      component: RandomMovieDetailView
    },
  ]
})


// 로그인 관련 페이지 막기 일단 주석 처리하기

/*
router.beforeEach((to, from) => {
  const store = useCounterStore()
  // 만약 이동하는 목적지가 메인 페이지이면서
  // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if (!store.isLogin && to.name !== 'LogInView' && to.name !== 'SignUpView') {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
  // 메인 페이지로 보냄
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'ArticleView' }
  }
})
*/
export default router;
