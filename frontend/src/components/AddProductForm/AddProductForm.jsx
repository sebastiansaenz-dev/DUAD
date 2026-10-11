import { useForm } from "react-hook-form";
import { useProductStore } from "../../store/useProductStore";
import styles from "./styles/AddProductForm.module.css";

const AddProductForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const { addProduct } = useProductStore();

  const onSubmit = (data) => {
    addProduct(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className={styles["product-form"]}>
      <div className={styles["form-group"]}>
        <label htmlFor="nombre">Nombre</label>
        <input
          id="nombre"
          placeholder="Nombre del producto"
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
          placeholder="Descripcion detallada del producto"
          {...register("descripcion", { required: "Campo obligatorio" })}
        />
        {errors.descripcion && (
          <span role="alert" className={styles["error-message"]}>
            {errors.descripcion.message}
          </span>
        )}
      </div>

      <div className={styles["form-row"]}>
        <div className={styles["form-group"]}>
          <label htmlFor="precio">Precio</label>
          <input
            id="precio"
            type="number"
            step="0.01"
            min="0"
            placeholder="0.00"
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
            placeholder="Cateogria del producto (ej. Alimento, Juguetes)"
            {...register("categoria", { required: "Campo obligatorio" })}
          />
          {errors.categoria && (
            <span role="alert" className={styles["error-message"]}>
              {errors.categoria.message}
            </span>
          )}
        </div>
      </div>

      <div className={styles["form-group"]}>
        <label htmlFor="imagen">URL de la imagen</label>
        <input
          id="imagen"
          type="url"
          placeholder="/api/placehold.co/600x400"
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
          placeholder="0"
          {...register("stock", { required: "Campo obligatorio" })}
        />
        {errors.stock && (
          <span role="alert" className={styles["error-message"]}>
            {errors.stock.message}
          </span>
        )}
      </div>
      <button className={styles["submit-btn"]} type="submit">
        Agregar producto
      </button>

      {Object.keys(errors).length > 0 && (
        <span role="alert" className={styles["error-message"]}>
          Por favor completa todos los campos antes de guardar los cambios
        </span>
      )}
    </form>
  );
};

export default AddProductForm;
