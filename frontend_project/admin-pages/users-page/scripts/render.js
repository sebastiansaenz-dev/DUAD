import { getEl, escapeHtml, capitalize, getPrimaryRole } from "./helpers.js";
import {
  getAllUsers,
  getRoleFilter,
  setRoleFilter,
  setCurrentPage,
  getCurrentPage,
  getTotalPages,
  getRoleCounts,
  getPagedUsers,
} from "./state.js";

export const renderAll = () => {
  renderRoleFilterList();
  renderUsersTable();
  renderPagination();
};

const renderRoleFilterList = () => {
  const roleCounts = getRoleCounts();
  const listEl = getEl("roleList");

  listEl.innerHTML =
    buildRoleFilterButton("all", "All", getAllUsers().length) +
    Object.keys(roleCounts)
      .sort()
      .map((role) =>
        buildRoleFilterButton(role, capitalize(role), roleCounts[role]),
      )
      .join("");

  attachRoleFilterListeners();
};

const buildRoleFilterButton = (value, label, count) => {
  const isActive = getRoleFilter() === value;
  const safeValue = value.replace(/"/g, "&quot;");
  return (
    '<li><button class="filter-btn ' +
    (isActive ? "active" : "") +
    '" data-role="' +
    safeValue +
    '">' +
    "<span>" +
    escapeHtml(label) +
    "</span>" +
    '<span class="filter-count">' +
    count +
    "</span>" +
    "</button></li>"
  );
};

const attachRoleFilterListeners = () => {
  document.querySelectorAll("#roleList .filter-btn").forEach((button) => {
    button.addEventListener("click", () => {
      setRoleFilter(button.getAttribute("data-role"));
      setCurrentPage(1);
      renderAll();
    });
  });
};

const renderUsersTable = () => {
  const visibleUsers = getPagedUsers();
  const hasResults = visibleUsers.length > 0;

  toggleEmptyState(!hasResults);
  if (!hasResults) {
    getEl("tableBody").innerHTML = "";
    return;
  }

  getEl("tableBody").innerHTML = visibleUsers.map(buildUserRow).join("");
};

const toggleEmptyState = (shouldShow) => {
  getEl("emptyState").style.display = shouldShow ? "block" : "none";
};

const buildUserRow = (user) => {
  return (
    '<tr data-id="' +
    user.id +
    '">' +
    '<td data-label="Username">' +
    escapeHtml(user.username) +
    "</td>" +
    '<td data-label="Email">' +
    escapeHtml(user.email) +
    "</td>" +
    '<td data-label="Role">' +
    buildRolePill(getPrimaryRole(user)) +
    "</td>" +
    '<td data-label="Actions">' +
    buildRowActions(user.id) +
    "</td>" +
    "</tr>"
  );
};

const buildRolePill = (role) => {
  const className = role ? role.toLowerCase() : "no-role";
  const label = role ? capitalize(role) : "No role";
  return (
    '<span class="role-pill ' + className + '">' + escapeHtml(label) + "</span>"
  );
};

const buildRowActions = (userId) => {
  return (
    '<div class="row-actions" style="justify-content:flex-end;">' +
    '<button class="icon-btn" data-action="edit" data-id="' +
    userId +
    '" aria-label="Edit">' +
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>' +
    "</button>" +
    '<button class="icon-btn danger" data-action="delete" data-id="' +
    userId +
    '" aria-label="Delete">' +
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>' +
    "</button>" +
    "</div>"
  );
};

const renderPagination = () => {
  getEl("prevPageBtn").disabled = getCurrentPage() <= 1;
  getEl("nextPageBtn").disabled = getCurrentPage() >= getTotalPages();
  getEl("paginationPages").innerHTML = buildPageNumbers();
  attachPaginationPageListeners();
};

const buildPageNumbers = () => {
  const pages = getPageNumbersToShow();

  return pages
    .map((page) => {
      if (page === "...") {
        return '<span class="pagination-ellipsis">…</span>';
      }
      const isActive = page === getCurrentPage();
      return (
        '<button type="button" class="pagination-page ' +
        (isActive ? "active" : "") +
        '" data-page="' +
        page +
        '">' +
        page +
        "</button>"
      );
    })
    .join("");
};

const getPageNumbersToShow = () => {
  const pages = [];
  const windowSize = 1;
  const total = getTotalPages();
  const current = getCurrentPage();

  for (let page = 1; page <= total; page++) {
    const isEdge = page === 1 || page === total;
    const isNearCurrent = Math.abs(page - current) <= windowSize;

    if (isEdge || isNearCurrent) {
      pages.push(page);
    } else if (pages[pages.length - 1] !== "...") {
      pages.push("...");
    }
  }

  return pages;
};

const attachPaginationPageListeners = () => {
  document.querySelectorAll(".pagination-page").forEach((button) => {
    button.addEventListener("click", () =>
      goToPage(Number(button.getAttribute("data-page"))),
    );
  });
};

const goToPage = (page) => {
  if (page < 1 || page > getTotalPages() || page === getCurrentPage()) return;
  setCurrentPage(page);
  renderAll();
};

export const goToPreviousPage = () => goToPage(getCurrentPage() - 1);
export const goToNextPage = () => goToPage(getCurrentPage() + 1);
