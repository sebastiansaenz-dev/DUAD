import { apiPublic } from "../../utils/utils.js";

export const loginRequest = async (email, password) => {
  const response = await apiPublic.post("/users/login", { email, password });
  return response.data;
};
