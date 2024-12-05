// src/api/auth.js

/*

로그인을 담당 api입니다.

signUp : 사용자로부터 입력받은 formData로 signup 요청
login : 사용자로부터 입력받은 loginData로 login 요청

*/

import axios from "axios";

const API_URL = "http://127.0.0.1:8000/accounts";

// 회원가입 API 요청
export const signUpUser = async (formData) => {
  try {
    const response = await axios.post(`${API_URL}/signup/`, formData, {
      header: {
        Accept: "application/json",
      },
    });
    return response.data; // 응답 데이터 반환
  } catch (error) {
    throw error; // 오류처리
  }
};

// 로그인 API 요청
export const loginUser = async (loginData) => {
  try {
    const response = await axios.post(`${API_URL}/login/`, loginData);
    return response.data; // 응답 데이터 반환
  } catch (error) {
    throw error; // 오류처리
  }
};
