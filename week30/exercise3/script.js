const radioYes = document.getElementById("radio-employee-yes");
const radioNo = document.getElementById("radio-employee-no");

const employmentSpace = () => {
  const employmentSection = document.getElementById("employment-section");
  employmentSection.innerHTML = "";
  if (radioYes.checked) {
    const employBox = document.createElement("input");

    employBox.placeholder = "enter your current employment";

    employmentSection.appendChild(employBox);
  }
};

radioYes.addEventListener("change", employmentSpace);
radioNo.addEventListener("change", employmentSpace);
