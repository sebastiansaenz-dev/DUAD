const button = document.getElementById("upload-data");

const printElements = () => {
  const input = document.getElementById("text");
  const printedElement = document.createElement("h1");
  const printedSection = document.getElementById("printed-items");

  printedSection.innerHTML = "";

  printedElement.innerHTML = input.value;

  printedSection.appendChild(printedElement);

  input.value = "";
};

button.addEventListener("click", printElements);
