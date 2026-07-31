export const checkAuth = () => {
  const user = localStorage.getItem("user");
  if (!user) {
    window.location.href = "../login-page/login.html";
    return null;
  }
  return JSON.parse(user);
};
