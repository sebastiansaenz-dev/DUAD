import axios from "axios";
import { getAuthUser, runLogout, setAuthUser } from "../context/AuthContext";

const BASE_URL = import.meta.env.VITE_API_URL;

export const api = axios.create({
  baseURL: BASE_URL,
});

export const apiAuth = axios.create({
  baseURL: BASE_URL + "/staff-portal/",
});

const goToLogin = () => {
  runLogout();
  if (window.location.pathname !== "/login") {
    window.location.assign("/login");
  }
};

const attachAccessToken = (request) => {
  if (request.headers.Authorization) {
    return request;
  }
  const accessToken = getAuthUser()?.access_token;
  if (accessToken) {
    request.headers.Authorization = `Bearer ${accessToken}`;
  }
  return request;
};

api.interceptors.request.use(attachAccessToken, (error) =>
  Promise.reject(error)
);

apiAuth.interceptors.request.use(attachAccessToken, (error) =>
  Promise.reject(error)
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

      const user = getAuthUser();
      if (!user?.refresh_token) {
        goToLogin();
        return Promise.reject(error);
      }

      try {
        const response = await api.post(
          "/refresh/",
          {},
          {
            headers: {
              Authorization: `Bearer ${user.refresh_token}`,
            },
          }
        );

        const updatedUser = {
          ...user,
          access_token: response.data.access_token,
        };
        setAuthUser(updatedUser);

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
