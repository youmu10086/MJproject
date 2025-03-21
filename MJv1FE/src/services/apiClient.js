// src/services/apiClient.js
import axios from "axios";
import { ElMessage } from "element-plus";

const apiClient = axios.create({
  baseURL: "/api", // 替换为您的 Django 后端 URL
  withCredentials: true, // 允许跨域请求携带 cookies
});

// 添加请求拦截器，自动附加 Access Token
apiClient.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    // 可以在这里处理请求错误
    return Promise.reject(error);
  }
);

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers["Authorization"] = `Bearer ${token}`;
            return apiClient(originalRequest);
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // 使用独立的 axios 实例刷新 Token
        const refreshClient = axios.create({
          baseURL: "/api",
          withCredentials: true,
        });

        const { data } = await refreshClient.post("refresh_token/");
        localStorage.setItem("accessToken", data.access);
        apiClient.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${data.access}`;

        processQueue(null, data.access);
        console;
        console.log("accessToken刷新成功");
        return apiClient(originalRequest);
      } catch (refreshError) {
        // 刷新失败处理

        localStorage.removeItem("accessToken");
        try {
          await apiClient.post("logout/");
        } catch (e) {}
        window.location.href = "/home";
        processQueue(refreshError, null);
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    if (error.response) {
      const { status, data } = error.response;

      // 优先使用后端返回的错误信息
      const errorMessage =
        data?.msg || getDefaultMessage(status) || "发生未知错误";

      // 特殊处理 401 状态码
      if (status === 401) {
        ElMessage.error(data?.msg || "请重新登录");
      } else {
        ElMessage.error(errorMessage);
      }
    } else {
      ElMessage.error("网络连接异常，请检查网络设置");
    }

    return Promise.reject(error);
  }
);

// 默认错误消息映射
const getDefaultMessage = (status) => {
  const messages = {
    400: "请求参数错误",
    403: "没有访问权限",
    404: "资源不存在",
    500: "服务器内部错误",
    502: "网关错误",
    503: "服务不可用",
    504: "网关超时",
  };
  return messages[status];
};
export default apiClient;
