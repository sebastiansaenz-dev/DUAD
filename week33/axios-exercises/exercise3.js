const axios = require("axios");

const productId = "ff8081819f7e10ae019f9fee0f3d2d7b";

const getProductById = async (id) => {
  try {
    const url = `https://api.restful-api.dev/objects/${id}`;

    const response = await axios.get(url);

    console.log(response.data);
  } catch (error) {
    console.log(error);
  }
};

getProductById(productId);
