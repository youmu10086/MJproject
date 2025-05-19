// stores/device.ts
import { defineStore } from "pinia";
import { ref, onMounted, onUnmounted, computed } from "vue";

export const useDeviceStore = defineStore("device", () => {
  const isMobile = ref(false);

  // 1. 初始检测（userAgent + 窗口宽度）
  const checkDevice = () => {
    const flag = navigator.userAgent.match(
      /(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i
    );
    const isWindowSizeMobile = window.innerWidth <= 768; // 辅助判断

    isMobile.value = !!flag || isWindowSizeMobile; // 优先用 userAgent，其次用窗口宽度
  };

  // 2. 监听窗口变化
  onMounted(() => {
    checkDevice(); // 初始化检测
    window.addEventListener("resize", checkDevice);
  });

  onUnmounted(() => {
    window.removeEventListener("resize", checkDevice);
  });

  // 3. 计算属性（可选）
  const isComputer = computed(() => !isMobile.value);

  return {
    isMobile,
    isComputer, // 可选，根据需求决定是否暴露
  };
});