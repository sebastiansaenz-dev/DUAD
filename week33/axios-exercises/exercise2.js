const axios = require("axios");

const productData = {
  name: "iPhone",
  data: {
    color: "white",
  },
};

const postData = async (data) => {
  const url = "https://api.restful-api.dev/objects";

  try {
    const response = await axios.post(url, data);

    console.log("Object created!");
    console.log(response.data);
  } catch (error) {
    console.error(`Error in the request: ${error}`);
  }
};

postData(productData);
