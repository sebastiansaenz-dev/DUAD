const checkAuth = () => {
  const user = localStorage.getItem("user");
  if (!user) {
    window.location.href = "../register-page/register.html";
    return null;
  }
  return JSON.parse(user);
};

const renderUserData = (userData) => {
  const cardsContainer = document.getElementById("card-container");

  const dataToProcess = {
    id: userData.id,
    name: userData.name,
    ...userData.data,
  };

  delete dataToProcess.password;

  for (const [key, value] of Object.entries(dataToProcess)) {
    const card = document.createElement("div");
    card.classList.add("card");

    const title = document.createElement("h3");
    title.textContent = key.toUpperCase();

    const text = document.createElement("p");
    text.textContent = value;

    card.appendChild(title);
    card.appendChild(text);
    cardsContainer.appendChild(card);
  }
};

const changePassword = () => {
  const changePasswordButton = document.getElementById(
    "change-password-button",
  );

  changePasswordButton.addEventListener("click", () => {
    window.location.href = "../change-password-page/change-password.html";
  });
};

const logOut = () => {
  const logOutButton = document.getElementById("log-out-button");

  logOutButton.addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "../login-page/login.html";
  });
};

const eventListeners = () => {
  changePassword();
  logOut();
};

const init = () => {
  const userData = checkAuth();
  if (!userData) return;
  renderUserData(userData);
  eventListeners();
};

init();
