const checkAuth = () => {
  const user = localStorage.getItem("user");
  if (!user) {
    window.location.href = "../login-page/login.html";
    return null;
  }
  return JSON.parse(user);
};

const updatePassword = async (userId, newPassowrd, currentUserData) => {
  const newData = {
    data: {
      ...currentUserData,
      password: newPassowrd,
    },
  };

  const url = `https://api.restful-api.dev/objects/${userId}`;

  const response = await axios.patch(url, newData);

  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response.data));
  }
  return response.data;
};

const changePassword = () => {
  const changeForm = document.getElementById("change-password-form");
  changeForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(changeForm);
    const rawData = Object.fromEntries(formData.entries());

    const {
      "current-password": currentPassword,
      "new-password": newPassoword,
      "confirm-password": confirmPassword,
    } = rawData;

    try {
      const user = checkAuth();
      if (!user) return;

      console.log(user);

      if (user.data?.password !== currentPassword) {
        alert("incorrect current password");
        return;
      }

      if (newPassoword !== confirmPassword) {
        alert("The password confirmation does not match your new password");
        return;
      }

      await updatePassword(user.id, newPassoword, user.data);
      alert("your password has been changed");
      window.location.href = "../profile-page/profile.html";
    } catch (error) {
      console.error(error);
    }
  });
};

const init = () => {
  changePassword();
};

init();
