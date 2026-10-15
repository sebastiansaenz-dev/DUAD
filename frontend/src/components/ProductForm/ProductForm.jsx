import { useForm } from "react-hook-form";

const ProductForm = ({
  initialValues = {},
  onSubmit,
  submitButtonText,
  onCancel,
  styles,
  resetAfterSubmit = false,
}) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      nombre: initialValues.name,
      descripcion: initialValues.description,
      precio: initialValues.price,
      categoria: initialValues.category,
      imagen: initialValues.image_url,
      stock: initialValues.stock,
    },
  });

  const handleFormSubmit = (data) => {
    onSubmit(data);

    if (resetAfterSubmit) {
      reset();
    }
  };

  return (
    <>
      {Object.keys(errors).length > 0 && (
        <span role="alert" className={styles["error-message"]}>
          Por favor completa todos los campos antes de guardar los cambios.
        </span>
      )}
      <form
        onSubmit={handleSubmit(handleFormSubmit)}
        className={styles["product-form"]}
      >
        <div className={styles["form-group"]}>
          <label htmlFor="name">Nombre</label>
          <input
            id="name"
            placeholder="Nombre del producto"
            {...register("name", { required: "Campo obligatorio" })}
          />
          {errors.nombre && (
            <span role="alert" className={styles["error-message"]}>
              {errors.nombre.message}
            </span>
          )}
        </div>

        <div className={styles["form-group"]}>
          <label htmlFor="description">Descripción</label>
          <textarea
            id="description"
            placeholder="Descripción detallada del producto"
            {...register("description", { required: "Campo obligatorio" })}
          />
          {errors.descripcion && (
            <span role="alert" className={styles["error-message"]}>
              {errors.descripcion.message}
            </span>
          )}
        </div>

        <div className={styles["form-row"]}>
          <div className={styles["form-group"]}>
            <label htmlFor="price">Precio</label>
            <input
              id="price"
              type="number"
              step="0.01"
              min="0"
              placeholder="0.00"
              {...register("price", { required: "Campo obligatorio" })}
            />
            {errors.precio && (
              <span role="alert" className={styles["error-message"]}>
                {errors.precio.message}
              </span>
            )}
          </div>
          <div className={styles["form-group"]}>
            <label htmlFor="category">Categoría</label>
            <input
              id="category"
              type="text"
              placeholder="Categoría del producto (ej. Alimento, Juguetes)"
              {...register("category", { required: "Campo obligatorio" })}
            />
            {errors.categoria && (
              <span role="alert" className={styles["error-message"]}>
                {errors.categoria.message}
              </span>
            )}
          </div>
        </div>

        <div className={styles["form-group"]}>
          <label htmlFor="image">URL de la imagen</label>
          <input
            id="image"
            type="url"
            placeholder="/api/placehold.co/600x400"
            {...register("image", { required: "Campo obligatorio" })}
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
            placeholder="0"
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
            type="button"
            className={styles["cancel-btn"]}
            onClick={() => {
              reset();
              if (onCancel) onCancel();
            }}
          >
            Cancelar
          </button>
          <button className={styles["submit-btn"]} type="submit">
            {submitButtonText}
          </button>
        </div>
      </form>
    </>
  );
};

export default ProductForm;
