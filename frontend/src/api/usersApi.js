import { api } from "./axiosClient";
import { useAuthStore } from "../store/useAuthStore";

export const loginRequest = (email, password) => {
  return api.post("/users/login", { email, password });
};

export const logoutRequest = () => {
  const refreshToken = useAuthStore.getState().user?.refresh_token;
  return api.post(
    "/users/logout",
    {},
    {
      headers: {
        Authorization: `Bearer ${refreshToken}`,
      },
    }
  );
};
