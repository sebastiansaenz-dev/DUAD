const button = document.getElementById("change-color-button");

const paragraph = document.getElementById("change-color-lorem");

const changeColor = () => {
  const colors = ["red", "blue", "green", "yellow", "cyan", "pink"];
  const randomIndex = Math.floor(Math.random() * colors.length);

  paragraph.style.backgroundColor = colors[randomIndex];
};

button.addEventListener("click", changeColor);
