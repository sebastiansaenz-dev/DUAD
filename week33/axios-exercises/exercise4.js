const axios = require("axios");

const productId = "ff8081819f7e10ae019f9fee0f3d2d7b";
const newProductData = {
  name: "iPad",
};

const updateData = async (id, data) => {
  try {
    const url = `https://api.restful-api.dev/objects/${id}`;

    const response = await axios.patch(url, data);

    console.log(response.data);
    console.log("product updated");
  } catch (error) {
    console.error(error);
  }
};

updateData(productId, newProductData);
