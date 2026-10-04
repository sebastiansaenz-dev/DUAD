import { getPrimaryRole } from "./helpers.js";

export const PAGE_SIZE = 20;
export const ROLE_OPTIONS = ["admin", "client"];

let allUsers = [];
let currentRoleFilter = "all";
let searchTerm = "";
let editingUserId = null;
let currentPage = 1;
let totalPages = 1;

export const setAllUsers = (users) => {
  allUsers = users;
};

export const getAllUsers = () => allUsers;

export const setRoleFilter = (value) => {
  currentRoleFilter = value;
};

export const getRoleFilter = () => currentRoleFilter;

export const setSearchTerm = (value) => {
  searchTerm = value;
};

export const setEditingUserId = (id) => {
  editingUserId = id;
};

export const getEditingUserId = () => editingUserId;

export const setCurrentPage = (page) => {
  currentPage = page;
};

export const getCurrentPage = () => currentPage;
export const getTotalPages = () => totalPages;

export const findUserById = (id) => allUsers.find((user) => user.id === id);

export const removeUserFromState = (id) => {
  allUsers = allUsers.filter((user) => user.id !== id);
};

export const applyUpdateToLocalUser = (id, updatedFields) => {
  const user = findUserById(id);
  if (!user) return;

  user.username = updatedFields.username ?? user.username;
  user.email = updatedFields.email ?? user.email;

  if (updatedFields.role) {
    user.roles = [{ id: user.roles?.[0]?.id, name: updatedFields.role }];
  }
};

export const getRoleCounts = () => {
  const counts = {};
  allUsers.forEach((user) => {
    const role = getPrimaryRole(user) || "no role";
    counts[role] = (counts[role] || 0) + 1;
  });
  return counts;
};

const matchesRoleFilter = (user) => {
  if (currentRoleFilter === "all") return true;
  return (getPrimaryRole(user) || "no role") === currentRoleFilter;
};

const matchesSearchTerm = (user) => {
  if (!searchTerm) return true;
  const term = searchTerm.toLowerCase();
  return (
    (user.username || "").toLowerCase().includes(term) ||
    (user.email || "").toLowerCase().includes(term)
  );
};

export const getFilteredUsers = () => {
  return allUsers.filter(
    (user) => matchesRoleFilter(user) && matchesSearchTerm(user),
  );
};

export const getPagedUsers = () => {
  const filtered = getFilteredUsers();
  totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  if (currentPage > totalPages) currentPage = totalPages;

  const start = (currentPage - 1) * PAGE_SIZE;
  return filtered.slice(start, start + PAGE_SIZE);
};
