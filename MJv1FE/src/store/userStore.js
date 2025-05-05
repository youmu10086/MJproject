import { defineStore } from "pinia";
import { ref, computed, watch, onMounted } from "vue";
import apiClient from "@/services/apiClient";

export const useUserStore = defineStore("user", () => {
  const validateRole = (value) =>
    ["guest", "customer", "manager", "admin"].includes(value);

  const getInitialState = () => ({
    isLoggedIn: localStorage.getItem("isLoggedIn") === "true",
    userInfo: JSON.parse(localStorage.getItem("userInfo") || "null") || {
      username: "",
      id: "",
    },
    role: "guest", // 初始化为 "guest"
  });

  const state = getInitialState();
  const isLoggedIn = ref(state.isLoggedIn);
  const role = ref(state.role);
  const userInfo = ref(state.userInfo);
  const loginDialogVisible = ref(false);

  // 持久化
  const persistState = () => {
    localStorage.setItem("isLoggedIn", isLoggedIn.value);
    localStorage.setItem("userInfo", JSON.stringify(userInfo.value));
  };
  watch([isLoggedIn, userInfo], persistState, { deep: true });

  const resetUser = () => {
    isLoggedIn.value = false;
    role.value = "guest";
    userInfo.value = { username: "", id: "" };
    ["isLoggedIn", "userInfo"].forEach((key) => localStorage.removeItem(key));
  };
  const fetchUserRole = async () => {
    try {
      const response = await apiClient.post("get_userRole/");
      if (response.status === 200) {
        const { role: userRole } = response.data;
        if (validateRole(userRole)) {
          role.value = userRole;
          return true; // 增加返回成功状态
        }
        return false;
      }
    } catch (error) {
      console.error("获取角色失败:", error);
      resetUser();
      throw error; // 抛出错误供调用方处理
    }
  };

  // 在组件挂载时自动检查并获取角色
  onMounted(async () => {
    if (isLoggedIn.value) {
      await fetchUserRole();
    }
  });

  return {
    isLoggedIn,
    userInfo,
    loginDialogVisible,
    role,
    resetUser,
    fetchUserRole, // 仍然导出 fetchUserRole 方法，以便在需要时调用
    isCustomer: computed(() => role.value === "customer"),
    isManager: computed(() => role.value === "manager"),
    isAdmin: computed(() => role.value === "admin"),
    isGuest: computed(() => role.value === "guest"),
  };
});
