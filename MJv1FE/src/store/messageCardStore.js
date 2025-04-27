import { defineStore } from "pinia";
import { ref } from "vue";

export const useMessageCardStore = defineStore("messageCard", () => {
  // 控制消息卡片的显示状态
  const messageCardIsDisplayed = ref(
    localStorage.getItem("isDisplay") === "true"
  );

  /**
   * 设置消息卡片的显示状态
   * @param {boolean} isDisplayed - 是否显示消息卡片
   */
  const setMessageCardDisplayed = (isDisplayed) => {
    messageCardIsDisplayed.value = isDisplayed;
    localStorage.setItem("isDisplay", isDisplayed.toString());
  };

  return {
    messageCardIsDisplayed,
    setMessageCardDisplayed,
  };
});