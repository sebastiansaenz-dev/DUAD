import { useState } from "react";
import { useForm } from "react-hook-form";
import styles from "./styles/Contact.module.css";

const Contact = () => {
  const [sent, setSent] = useState(false);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm();

  const onSubmit = () => {
    setSent(true);
    reset();
  };

  return (
    <main className={styles["page"]}>
      <form onSubmit={handleSubmit(onSubmit)} className={styles["form"]}>
        <h1 className={styles["form-title"]}>Contacto</h1>
        <p className={styles["form-intro"]}>
          ¿Tienes una pregunta o sugerencia? Escríbenos y te responderemos lo
          antes posible.
        </p>

        {sent && (
          <p className={styles["success-message"]}>
            Tu mensaje se envió correctamente. Gracias por contactarnos.
          </p>
        )}

        <div className={styles["input-container"]}>
          <label htmlFor="name">Nombre completo</label>
          <input
            type="text"
            id="name"
            {...register("name", {
              required: "Campo obligatorio",
              validate: (value) => value.trim() !== "" || "Campo obligatorio",
            })}
          />
          {errors.name && (
            <span role="alert" className={styles["error-message"]}>
              {errors.name.message}
            </span>
          )}
        </div>

        <div className={styles["input-container"]}>
          <label htmlFor="email">Correo electrónico</label>
          <input
            type="email"
            id="email"
            {...register("email", {
              required: "Campo obligatorio",
              validate: (value) => value.trim() !== "" || "Campo obligatorio",
              pattern: {
                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: "Ingresa un email válido",
              },
            })}
          />
          {errors.email && (
            <span role="alert" className={styles["error-message"]}>
              {errors.email.message}
            </span>
          )}
        </div>

        <div className={styles["input-container"]}>
          <label htmlFor="type">Asunto</label>
          <select
            id="type"
            defaultValue=""
            {...register("type", { required: "Campo obligatorio" })}
          >
            <option value="" disabled>
              Selecciona una opción
            </option>
            <option value="question">Pregunta</option>
            <option value="suggestion">Sugerencia</option>
          </select>
          {errors.type && (
            <span role="alert" className={styles["error-message"]}>
              {errors.type.message}
            </span>
          )}
        </div>

        <div className={styles["input-container"]}>
          <label htmlFor="message">Mensaje</label>
          <textarea
            id="message"
            rows="5"
            {...register("message", {
              required: "Campo obligatorio",
              validate: (value) => value.trim() !== "" || "Campo obligatorio",
            })}
          />
          {errors.message && (
            <span role="alert" className={styles["error-message"]}>
              {errors.message.message}
            </span>
          )}
        </div>

        <button className={styles["submit"]} type="submit">
          Enviar mensaje
        </button>
      </form>
    </main>
  );
};

export default Contact;
