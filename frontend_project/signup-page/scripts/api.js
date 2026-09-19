import { apiPublic } from "../../utils/utils.js";

export const registerUserRequest = async (username, email, password) => {
  const response = await apiPublic.post("/users/register-user", {
    username,
    email,
    password,
  });
  return response.data;
};
