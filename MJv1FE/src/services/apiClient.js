// src/services/apiClient.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: "/api", // 替换为您的 Django 后端 URL
  withCredentials: true, // 允许跨域请求携带 cookies
});

// 添加请求拦截器，自动附加 Access Token
apiClient.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem("accessToken");
  if (accessToken) {
    config.headers["Authorization"] = `Bearer ${accessToken}`;
  }
  return config;
});

export default apiClient;
