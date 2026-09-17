const productId = "ff8081819f7e10ae019f9a9a93c4282c";
const newProductData = {
  name: "iPad",
};

const updateData = async (id, data) => {
  try {
    const requestOptions = {
      method: "PATCH",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify(data),
    };

    const url = `https://api.restful-api.dev/objects/${id}`;

    const response = await fetch(url, requestOptions);

    if (!response.ok) {
      throw Error("there was an error connecting to the server");
    }

    const responseData = await response.json();

    console.log(data);
    console.log("product updated");
  } catch (error) {
    console.error(error);
  }
};

updateData(productId, newProductData);
