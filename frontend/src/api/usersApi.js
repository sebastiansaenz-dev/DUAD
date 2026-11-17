import { api } from "./axiosClient";
import { getAuthUser } from "../context/AuthContext";

export const loginRequest = (email, password) => {
  return api.post("/users/login", { email, password });
};

export const logoutRequest = () => {
  const user = getAuthUser();
  return api.post(
    "/users/logout",
    {},
    {
      headers: {
        Authorization: `Bearer ${user?.refresh_token}`,
      },
    }
  );
};
