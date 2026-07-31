import { checkAuth } from "../utils/check-auth";

const updatePassword = async (userId, newPassowrd, currentUserData) => {
  const newData = {
    data: {
      ...currentUserData,
      password: newPassword,
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
      "new-password": newPassword,
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

      if (newPassword !== confirmPassword) {
        alert("The password confirmation does not match your new password");
        return;
      }

      await updatePassword(user.id, newPassword, user.data);
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
