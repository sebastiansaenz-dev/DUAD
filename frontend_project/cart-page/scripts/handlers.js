import { showErrorMessage } from "../../utils/utils.js";
import { removeFromCartRequest } from "./api.js";

export const removeProductFromCart = async (productId, onSuccess) => {
  try {
    await removeFromCartRequest(productId);
    onSuccess();
  } catch (error) {
    showErrorMessage(error);
  }
};
