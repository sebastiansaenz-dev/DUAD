const productData = {
  name: "iPhone",
  data: {
    color: "white",
  },
};

const postData = async (data) => {
  const requestOptions = {
    method: "POST",
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

  const url = "https://api.restful-api.dev/objects";

  try {
    const response = await fetch(url, requestOptions);

    if (!response.ok) {
      throw Error(`There was an error: ${response.statusText}`);
    }

    const result = await response.json();

    console.log("Object created!");
    console.log(result);

    return result;
  } catch (error) {
    console.error(`Error in the request: ${error}`);
  }
};

postData(productData);
