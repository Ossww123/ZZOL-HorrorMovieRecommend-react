# Project. ZZOL

---

### 팀원 : 최재영, 오승우

----    

#### 배경

---

영화 추천 서비스는 널리고 널렸다. 하지만 특정 장르의 영화를 검색하게 되면 대부분 블로그나 유튜브를 통해 추천을 받을 수 밖에 없는 현실.

```
---

### 어떻게?

---

1️⃣ **기술 스택은 무엇을 사용 할 것인가?**

> ***Django + js** 혹은 **DRF + Vue.js***

2️⃣ **각자 맡을 업무는 무엇인가?**

    최재영 : 백엔드, 오승우: 프론트

3️⃣ **인증 서비스는 어떻게 구현할 것인가?**

    Django Authentication 이용

4️⃣ **DB는 어떤 정보를 기반으로 할 것인가?**

    TMDB API 서비스에서 키워드를 기반

5️⃣ **목적에 맞는 서비스를 구현하기 위해 모델링은 어떻게 구성하여야 할 것인가?**

---
```

---

# 진행 상황 공유

---

2024.11.18 17:35
back 

project settings.py 설정 완료

accounts 설정 완료
model 설정 중 중단



---



2024.11.23 21:35

만진거
App.vue
LogInView.vue
SignUpView.vue
MovieRecommend.vue
MovieDetailInfo.vue
ReviewSearchView.vue
ArticleView.vue
ArticleList.vue
ArticleListItem.vue

Canvas.vue 추가

공포 테마의 CSS 추가
추천 알고리즘에 이미지 돌아가게 하는거에 시간 갈아넣음
=======
2024.11.23 17:18

back

인기 최신 평점 공포순으로 출력되게끔 데이터 연동 성공
(공포점수는 유저가 직접줘야 반영되서 초기 데이터 만들것)
-> MovieListView.vue에 일단 명령어랑 콘솔 찍어놨음

랜덤 키워드 영화 추가
view에서 딕셔너리 형태로 탐색하는 기능 추가
vue.store에 랜덤 뽑아내는 기능 추가
vue.index랑 vue.views에 확인용 random 관련 명령어 추가

배우, 감독출력 기능 추가
db 받을 당시 상위 몇멍을 제한을 걸어
감독은 1명, 배우는 5명 출력 가능함 
추가적으로 출력하고 싶다면 back.views.py 에서 수정해야함

=========

2024.11.25 03:00

back

db에 없는 데이터들은 받아서 저장한 다음 출력할 수 있게 만듬
그에 맞춘 views, urls, components 및 vue 추가

수정해야될 부분
추가된 부분 리뷰 생성시 리뷰 출력 안됨
평점이 리뷰 생성할때는 즉시 반영 되는데, 삭제할때는 반영이 안됨
강제로 새로고침을 유발해서 동기로 끌어오려해도 가져오는데 시간이 걸리는건지 잔상 데이터가 남아있음

