const getlogin = () => {
  const user = loginForm.value;

  apiClient
    .post("login/", user)
    .then((res) => {
      userStore.userInfo.name = res.data.username;
      userStore.updateLoginStatus(true);
      localStorage.setItem("accessToken", res.data.access);

      userStore.loginDialogVisible = false; // 登录成功后关闭对话框
      ElMessage.success("登录成功");
    })
    .catch((err) => {
      console.error(err);
      // 此处可以添加用户通知，例如使用 Element Plus 的 ElNotification
    });
};

// 注册逻辑
const getenroll = () => {
  const user = loginForm.value;

  apiClient
    .post("enroll/", user)
    .then((res) => {
      userStore.userInfo.name = res.data.username;
      userStore.updateLoginStatus(true);
      localStorage.setItem("accessToken", res.data.access);
      userStore.loginDialogVisible = false; // 注册成功后关闭对话框
    })
    .catch((err) => {
      console.error(err);
      // 处理注册失败的通知
    });
};
