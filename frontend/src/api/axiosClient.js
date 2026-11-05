import axios from "axios";
import { useAuthStore } from "../store/useAuthStore";
import { usePageStore } from "../store/usePageStore";

const BASE_URL = "http://localhost:5002";

export const api = axios.create({
  baseURL: BASE_URL,
});

export const apiAuth = axios.create({
  baseURL: BASE_URL + "/staff-portal/",
});

const goToLogin = () => {
  useAuthStore.getState().logout();
  usePageStore.getState().setCurrentPage("login");
};

apiAuth.interceptors.request.use(
  (request) => {
    const accessToken = useAuthStore.getState().user?.access_token;
    if (accessToken) {
      request.headers.Authorization = `Bearer ${accessToken}`;
    }
    return request;
  },
  (error) => Promise.reject(error)
);

apiAuth.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      const userData = useAuthStore.getState().user;
      if (!userData?.refresh_token) {
        goToLogin();
        return Promise.reject(error);
      }

      try {
        const response = await api.post(
          "/refresh/",
          {},
          {
            headers: {
              Authorization: `Bearer ${userData.refresh_token}`,
            },
          }
        );

        const updatedUser = {
          ...userData,
          access_token: response.data.access_token,
        };
        useAuthStore.getState().login(updatedUser);

        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers.Authorization = `Bearer ${updatedUser.access_token}`;
        return apiAuth(originalRequest);
      } catch (refreshError) {
        goToLogin();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
