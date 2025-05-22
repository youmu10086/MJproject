declare module '@/store/userStore' {
  export interface UserInfo {
    id: string | number;
    username?: string;
    [key: string]: any;
  }
  export interface UserStore {
    userInfo: UserInfo;
    role: string;
    isLoggedIn: boolean;
    loginDialogVisible: boolean;
    [key: string]: any;
  }
  export function useUserStore(): UserStore;
}

declare module '@/services/apiClient' {
  import { AxiosInstance } from 'axios';
  const apiClient: AxiosInstance;
  export default apiClient;
}

declare module 'crypto-js' {
  const CryptoJS: any;
  export default CryptoJS;
}