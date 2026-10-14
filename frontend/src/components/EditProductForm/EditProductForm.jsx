import { useForm } from "react-hook-form";
import { useProductStore } from "../../store/useProductStore";
import styles from "./styles/EditProductForm.module.css";

const EditProductForm = ({ product, setCurrentPage }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      nombre: product.name,
      descripcion: product.description,
      precio: product.price,
      categoria: product.category,
      imagen: product.image_url,
      stock: product.stock,
    },
  });

  const { updateProduct } = useProductStore();

  const onSubmit = (data) => {
    const formattedProduct = {
      id: Number(product.id),
      name: data.nombre,
      description: data.descripcion,
      price: Number(data.precio),
      category: data.categoria,
      image_url: data.imagen,
      stock: Number(data.stock),
    };

    updateProduct(formattedProduct);
    setCurrentPage("administration");
  };

  return (
    <>
      {Object.keys(errors).length > 0 && (
        <span role="alert" className={styles["error-message"]}>
          Por favor completa todos los campos antes de guardar los cambios
        </span>
      )}
      <form
        onSubmit={handleSubmit(onSubmit)}
        className={styles["product-form"]}
      >
        <div className={styles["form-group"]}>
          <label htmlFor="nombre">Nombre</label>
          <input
            id="nombre"
            {...register("nombre", { required: "Campo obligatorio" })}
          />
          {errors.nombre && (
            <span role="alert" className={styles["error-message"]}>
              {errors.nombre.message}
            </span>
          )}
        </div>

        <div className={styles["form-group"]}>
          <label htmlFor="descripcion">Descripcion</label>
          <textarea
            id="descripcion"
            {...register("descripcion", { required: "Campo obligatorio" })}
          />
          {errors.descripcion && (
            <span role="alert" className={styles["error-message"]}>
              {errors.descripcion.message}
            </span>
          )}
        </div>

        <div className={styles["form-group"]}>
          <label htmlFor="precio">Precio</label>
          <input
            id="precio"
            type="number"
            step="0.01"
            min="0"
            {...register("precio", { required: "Campo obligatorio" })}
          />
          {errors.precio && (
            <span role="alert" className={styles["error-message"]}>
              {errors.precio.message}
            </span>
          )}
        </div>
        <div className={styles["form-group"]}>
          <label htmlFor="categoria">Categoria</label>
          <input
            id="categoria"
            type="text"
            {...register("categoria", { required: "Campo obligatorio" })}
          />
          {errors.categoria && (
            <span role="alert" className={styles["error-message"]}>
              {errors.categoria.message}
            </span>
          )}
        </div>

        <div className={styles["form-group"]}>
          <label htmlFor="imagen">URL de la imagen</label>
          <input
            id="imagen"
            type="url"
            {...register("imagen", { required: "Campo obligatorio" })}
          />
          {errors.imagen && (
            <span role="alert" className={styles["error-message"]}>
              {errors.imagen.message}
            </span>
          )}
        </div>

        <div className={styles["form-group"]}>
          <label htmlFor="stock">Stock</label>
          <input
            id="stock"
            type="number"
            step="1"
            min="0"
            {...register("stock", { required: "Campo obligatorio" })}
          />
          {errors.stock && (
            <span role="alert" className={styles["error-message"]}>
              {errors.stock.message}
            </span>
          )}
        </div>

        <div className={styles["form-btns"]}>
          <button
            className={styles["cancel-btn"]}
            onClick={(e) => {
              e.preventDefault();
              setCurrentPage("administration");
            }}
          >
            Cancelar
          </button>
          <button className={styles["submit-btn"]} type="submit">
            Guardar cambios
          </button>
        </div>
      </form>
    </>
  );
};

export default EditProductForm;
