const axios = window.axios;

export const api = axios.create({
  baseURL: "http://localhost:5002",
});

export const apiPublic = axios.create({
  baseURL: "http://localhost:5002",
});

const getTokenExpiration = (token) => {
  try {
    const payload = token.split(".")[1];
    const decoded = JSON.parse(atob(payload));
    return decoded.exp * 1000;
  } catch (error) {
    return null;
  }
};

const isTokenExpired = (token) => {
  const expiration = getTokenExpiration(token);
  if (!expiration) return true;
  return Date.now() >= expiration;
};

const isAdminUser = (userData) => {
  const roles = userData.user?.roles || userData.roles || [];
  return roles.some((role) => role.name === "admin");
};

export const logout = () => {
  localStorage.removeItem("user");
  window.location.href = "../login-page/login.html";
};

export const setUpLogoutButton = (buttonId = "logoutBtn") => {
  const button = document.getElementById(buttonId);
  if (!button) return;
  button.addEventListener("click", logout);
};

export const protectAdminRoute = () => {
  const user = localStorage.getItem("user");
  if (!user) {
    window.location.href = "../login-page/login.html";
    return;
  }

  try {
    const userData = JSON.parse(user);

    if (!isAdminUser(userData)) {
      window.location.href = "../landing-page/home.html";
    }
  } catch (error) {
    localStorage.removeItem("user");
    window.location.href = "../login-page/login.html";
  }
};

api.interceptors.request.use(
  (request) => {
    const userString = localStorage.getItem("user");
    if (userString) {
      const userData = JSON.parse(userString);
      if (userData.access_token) {
        request.headers.Authorization = `Bearer ${userData.access_token}`;
      }
    }
    return request;
  },
  (error) => Promise.reject(error),
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const userString = localStorage.getItem("user");
        if (!userString) {
          window.location.href = "../login-page/login.html";
          return Promise.reject(error);
        }

        const userData = JSON.parse(userString);
        const refreshToken = userData.refresh_token;

        if (isTokenExpired(refreshToken)) {
          console.error("Refresh token expired - session ended");
          localStorage.removeItem("user");
          window.location.href = "../login-page/login.html";
          return Promise.reject(new Error("Refresh token expired"));
        }

        const response = await apiPublic.post(
          "/refresh/",
          {},
          {
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          },
        );

        const newAccessToken = response.data.access_token;

        userData.access_token = newAccessToken;
        localStorage.setItem("user", JSON.stringify(userData));

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (error) {
        console.error("Cannot refresh token:", error.message);
        localStorage.removeItem("user");
        window.location.href = "../login-page/login.html";
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  },
);

export const checkAuth = () => {
  const user = localStorage.getItem("user");
  if (!user) {
    return null;
  }
  return JSON.parse(user);
};

export const showErrorMessage = (error) => {
  const errorSection = document.getElementById("error-section");

  const errorMessage =
    error.response?.data?.error?.message ||
    "There was an error. Please try again.";

  errorSection.textContent = errorMessage;
  errorSection.style.display = "block";
};

export const showUserType = () => {
  const user = checkAuth();
  const cartLogoContainer = document.getElementById("cart-logo-container");

  if (!user) {
    const logInButton = document.createElement("button");
    logInButton.classList.add("nav-button");
    logInButton.textContent = "Log In";

    logInButton.addEventListener("click", () => {
      window.location.href = "../login-page/login.html";
    });

    cartLogoContainer.appendChild(logInButton);
    return;
  }

  addAdminLinkIfNeeded(user);

  if (cartLogoContainer) {
    cartLogoContainer.innerHTML = "";
    const anchorTag = document.createElement("a");
    anchorTag.href = "../cart-page/cart.html";

    const svgElement = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "svg",
    );
    svgElement.setAttribute("version", "1.1");
    svgElement.setAttribute("id", "Layer_1");
    svgElement.setAttribute("viewBox", "0 0 95 118.8");
    svgElement.setAttribute("xml:space", "preserve");

    const pathElement = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "path",
    );
    pathElement.setAttribute(
      "d",
      "M49.5,72.8c3.5,0,6.3,2.8,6.3,6.3c0,3.5-2.8,6.3-6.3,6.3c-3.5,0-6.3-2.8-6.3-6.3c0-1.7,0.7-3.3,1.9-4.5 C46.2,73.5,47.8,72.8,49.5,72.8z M76,72.8c3.5,0,6.3,2.8,6.3,6.3s-2.8,6.3-6.3,6.3c-3.5,0-6.3-2.8-6.3-6.3c0-1.7,0.7-3.2,1.8-4.4 C72.8,73.5,74.4,72.8,76,72.8z M43.7,60.1c-0.1,0-0.1,0-0.2,0c-1,0.2-1.9,0.6-2.5,1.4c-1.5,1.7-1.3,4.4,0.5,5.8c0.7,0.6,1.7,1,2.7,1 h40c1-0.1,1.9,0.7,1.9,1.7s-0.7,1.9-1.7,1.9c-0.1,0-0.2,0-0.3,0h-40c-4.3,0-7.7-3.4-7.7-7.7c0-1.8,0.6-3.5,1.8-4.9 c-0.4-0.2-0.8-0.4-1.2-0.7c-1.4-1-2.4-2.4-2.9-4L20.6,16.2c-0.3-0.9-0.9-1.7-1.6-2.2c-0.8-0.5-1.7-0.8-2.6-0.8h-12 c-1,0.1-1.9-0.7-1.9-1.7c-0.1-1,0.7-1.9,1.7-1.9c0.1,0,0.2,0,0.3,0h12c3.5,0,6.5,2.2,7.7,5.4l3.5,10c0.1,0,0.2,0,0.3,0h62.9 c0.2,0,0.4,0,0.6,0.1c0.9,0.3,1.4,1.3,1.1,2.3l-9.5,27.3c-1.1,3.3-4.2,5.5-7.6,5.4H43.7z",
    );

    svgElement.appendChild(pathElement);
    anchorTag.appendChild(svgElement);
    cartLogoContainer.appendChild(anchorTag);

    const logoutButton = document.createElement("button");
    logoutButton.classList.add("nav-button");
    logoutButton.id = "logout-button";
    logoutButton.textContent = "Log Out";
    logoutButton.addEventListener("click", logout);
    cartLogoContainer.appendChild(logoutButton);
  }
};

const addAdminLinkIfNeeded = (userData) => {
  if (!isAdminUser(userData)) {
    if (document.getElementById("user-panel-link")) return;
    const navLinks = document.querySelector(".nav-links");
    if (!navLinks) return;

    const userItem = document.createElement("li");
    userItem.classList.add("nav-link");

    const userAnchor = document.createElement("a");
    userAnchor.id = "user-panel-link";

    userAnchor.href = "../user-page/profile.html";
    userAnchor.textContent = "Profile";

    userItem.appendChild(userAnchor);
    navLinks.appendChild(userItem);
  } else {
    if (document.getElementById("admin-panel-link")) return;

    const navLinks = document.querySelector(".nav-links");
    if (!navLinks) return;

    const adminItem = document.createElement("li");
    adminItem.classList.add("nav-links");

    const adminAnchor = document.createElement("a");
    adminAnchor.id = "admin-panel-link";

    adminAnchor.href = "../admin-pages/edit-products-page/products.html";
    adminAnchor.textContent = "Admin Panel";

    adminItem.appendChild(adminAnchor);
    navLinks.appendChild(adminItem);
  }
};

export const activePage = () => {
  document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll(".nav-link");

    navItems.forEach((item) => {
      const link = item.querySelector("a");
      const href = link.getAttribute("href");

      if (!href || href === "#") return;

      const currentFileName = currentPath.split("/").pop();
      const targetFileName = href.split("/").pop();

      if (currentFileName === targetFileName) {
        item.classList.add("active");
        if (item.tagName !== "LI") {
          item.closest("li")?.classList.add("active");
        }
      }
    });
  });
};

export const checkEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    showErrorMessage({ message: "Please enter a valid email" });
    return false;
  }
  return true;
};

export const checkPassword = (password) => {
  const minPasswordLength = 8;
  if (password.length < minPasswordLength) {
    showErrorMessage({
      message: "Password must have at least 8 characters long",
    });
    return false;
  }
  return true;
};
