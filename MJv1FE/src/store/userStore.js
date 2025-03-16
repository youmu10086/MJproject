import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";

export const useUserStore = defineStore("user", () => {
  // 类型验证简化为运行时检查
  const validateRole = (value) => ["customer", "manager"].includes(value);

  const getInitialState = () => ({
    isLoggedIn: localStorage.getItem("isLoggedIn") === "true",
    role: validateRole(localStorage.getItem("role")) ? localStorage.getItem("role") : "customer",
    userInfo: JSON.parse(localStorage.getItem("userInfo") || "null") || {
      name: "",
      contact: "",
    },
  });

  // 响应式状态
  const state = getInitialState();
  const isLoggedIn = ref(state.isLoggedIn);
  const role = ref(state.role);
  const userInfo = ref(state.userInfo);
  const loginDialogVisible = ref(false);

  // 自动持久化逻辑
  const persistState = () => {
    localStorage.setItem("isLoggedIn", isLoggedIn.value);
    localStorage.setItem("role", role.value);
    localStorage.setItem("userInfo", JSON.stringify(userInfo.value));
  };
  watch([isLoggedIn, role, userInfo], persistState, { deep: true });

  // 业务方法
  const resetUser = () => {
    isLoggedIn.value = false;
    role.value = "";
    userInfo.value = { name: "", contact: "" };
    ["isLoggedIn", "userInfo"].forEach((key) =>
      localStorage.removeItem(key)
    );
  };

  return {
    isLoggedIn,
    userInfo,
    loginDialogVisible,
    role,
    resetUser,
    isCustomer: computed(() => role.value === "customer"),
    isManager: computed(() => role.value === "manager"),
  };
});
