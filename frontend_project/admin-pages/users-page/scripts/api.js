import { api } from "../../../utils/utils.js";

export const getUsers = async () => {
  const response = await api.get("/staff-portal/users/");
  return Array.isArray(response.data) ? response.data : [];
};

export const updateUserRequest = async (id, payload) => {
  const url = `/staff-portal/users/${id}`;
  const response = await api.patch(url, payload);
  return response.data;
};

export const deleteUserRequest = async (id) => {
  const url = `/staff-portal/users/${id}`;
  const response = await api.delete(url);
  return response.data;
};
