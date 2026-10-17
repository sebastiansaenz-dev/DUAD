import { useForm } from "react-hook-form";

const ProductForm = ({
  initialValues = {},
  onSubmit,
  submitButtonText,
  onCancel,
  styles,
  resetAfterSubmit = false,
  errorMessage,
}) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      name: initialValues.name,
      description: initialValues.description,
      price: initialValues.price,
      category: initialValues.category,
      image: initialValues.image_url,
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
          {errorMessage}
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
          {errors.name && (
            <span role="alert" className={styles["error-message"]}>
              {errors.name.message}
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
          {errors.description && (
            <span role="alert" className={styles["error-message"]}>
              {errors.description.message}
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
            {errors.price && (
              <span role="alert" className={styles["error-message"]}>
                {errors.price.message}
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
            {errors.category && (
              <span role="alert" className={styles["error-message"]}>
                {errors.category.message}
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
          {errors.image && (
            <span role="alert" className={styles["error-message"]}>
              {errors.image.message}
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
