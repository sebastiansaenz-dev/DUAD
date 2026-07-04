import namer from "https://esm.sh/color-namer";

const div = document.getElementById("div-change-color");
const button = document.getElementById("change-color-button");

const colors = ["#FF5733", "#33FF57", "#3357FF", "#F5FF33", "#FF33F6"];

const showColorName = (colorCode) => {
  const colorName = namer(colorCode);

  div.innerHTML = "";

  const showName = document.createElement("p");

  showName.innerHTML = colorName.basic[0].name;

  div.appendChild(showName);
};

const changeColor = () => {
  const randomIndex = Math.floor(Math.random() * colors.length);
  div.style.backgroundColor = colors[randomIndex];
  showColorName(colors[randomIndex]);
};

button.addEventListener("click", changeColor);
