export const formatPrice = (price) => {
  return new Intl.NumberFormat("es-CR", {
    style: "currency",
    currency: "CRC",
    maximumFractionDigits: 0,
  }).format(price);
};

export const adaptProducts = (rawProducts) => {
  return rawProducts.map((product) => ({
    id: product.id,
    name: product.nombre || product.name,
    description: product.descripcion || product.description,
    price: product.precio || product.price,
    category: product.categoria || product.category,
    image_url: product.imagen || product.image_url,
    stock: product.stock || product.stock,
  }));
};
