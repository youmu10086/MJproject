// src/services/apiClient.js
import axios from "axios";
import { ElMessage, ElLoading, LoadingParentElement } from "element-plus";
import { ComponentPublicInstance, ComponentOptionsBase, ComponentProvideOptions, Ref } from "vue";

let loadingInstance: { close: any; setText?: (text: string) => void; removeElLoadingChild?: () => void; handleAfterLeave?: () => void; vm?: ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>>; $el?: HTMLElement; originalPosition?: Ref<string, string>; originalOverflow?: Ref<string, string>; visible?: Ref<boolean, boolean>; parent?: Ref<LoadingParentElement, LoadingParentElement>; background?: Ref<string, string>; svg?: Ref<string, string>; svgViewBox?: Ref<string, string>; spinner?: Ref<string | boolean, string | boolean>; text?: Ref<string, string>; fullscreen?: Ref<boolean, boolean>; lock?: Ref<boolean, boolean>; customClass?: Ref<string, string>; target?: Ref<HTMLElement, HTMLElement>; beforeClose?: Ref<(() => boolean) | undefined, (() => boolean) | undefined> | undefined; closed?: Ref<(() => void) | undefined, (() => void) | undefined> | undefined; } | null = null; // 存储全局加载实例

const apiClient = axios.create({
  baseURL: "/api", // API 基础路径
  withCredentials: true, // 允许跨域请求携带 cookies
  timeout: 10000, // 请求超时时间
  headers: {
    "Content-Type": "application/json", // 默认请求头
  },
});

// 添加请求拦截器，自动附加 Access Token
apiClient.interceptors.request.use(
  (config) => {
    // 启动全局加载
    loadingInstance = ElLoading.service({
      lock: true,
      background: "rgba(0, 0, 0, 0)",
    });

    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) config.headers["Authorization"] = `Bearer ${accessToken}`;
    return config;
  },
  (error) => {
    if (loadingInstance) loadingInstance.close(); // 关闭加载
    return Promise.reject(error);
  }
);

let isRefreshing = false; // 是否正在刷新 Token
let failedQueue: { resolve: (value: unknown) => void; reject: (reason?: any) => void; }[] = []; // 存储等待刷新 Token 的请求队列

const processQueue = (error: unknown, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

// 添加响应拦截器，处理错误和 Token 刷新逻辑
apiClient.interceptors.response.use(
  (response) => {
    if (loadingInstance) loadingInstance.close(); // 关闭加载
    return response;
  },
  async (error) => {
    if (loadingInstance) loadingInstance.close(); // 关闭加载
    const originalRequest = error.config;

    // 如果返回 401 且请求未重试，则尝试刷新 Token
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

    // 处理其他错误
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

const getDefaultMessage = (status: 400 | 403 | 404 | 500 | 502 | 503 | 504) => {
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
