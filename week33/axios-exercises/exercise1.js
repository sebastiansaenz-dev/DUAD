const axios = require("axios");

const getData = async () => {
  try {
    const response = await axios.get("https://api.restful-api.dev/objects");

    const validObjects = response.data.filter((item) => item.data);

    validObjects.forEach((item, index) => {
      console.log(`\n[${index + 1}] ID: ${item.id} | Product: ${item.name}`);
      console.log("Details:");

      for (const [key, value] of Object.entries(item.data)) {
        console.log(`${key}: ${value}`);
      }
    });
  } catch (error) {
    console.log(error);
  }
};

getData();
