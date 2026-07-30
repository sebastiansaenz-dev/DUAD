const productId = "ff8081819f7e10ae019f9a9a93c4282c";

const getProductById = async (id) => {
  try {
    const url = `https://api.restful-api.dev/objects/${id}`;

    const response = await fetch(url);

    if (!response.ok) {
      throw Error("there was an error connecting to the server");
    }

    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.log(error);
  }
};

getProductById(productId);
