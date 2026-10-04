import { apiPublic } from "../../utils/utils.js";

export const getProductsRequest = async (page = 1, search = "") => {
  let url = `/products/?page=${page}`;
  if (search) {
    url += `&name=${encodeURIComponent(search)}`;
  }
  const response = await apiPublic.get(url);
  return response.data;
};
