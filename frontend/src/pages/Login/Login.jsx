import { useState } from "react";
import { useForm } from "react-hook-form";
import { loginRequest } from "../../api/usersApi";
import { useAuthStore } from "../../store/useAuthStore";
import Loader from "../../components/loading-ui/Loader";
import styles from "./styles/Login.module.css";

const Login = ({ setCurrentPage }) => {
  const login = useAuthStore((state) => state.login);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (formData) => {
    setLoading(true);
    setError(null);

    loginRequest(formData.email, formData.password)
      .then((res) => {
        login(res.data);
        setCurrentPage("home");
      })
      .catch((err) =>
        setError(err.response?.data?.error?.message || err.message)
      )
      .finally(() => setLoading(false));
  };

  if (loading) {
    return (
      <main className={styles["page"]}>
        <Loader />
      </main>
    );
  }

  return (
    <main className={styles["page"]}>
      <form onSubmit={handleSubmit(onSubmit)} className={styles["form"]}>
        <h2 className={styles["form-title"]}>Iniciar sesión</h2>
        {error && <p className={styles["error-message"]}>{error}</p>}
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
          <label htmlFor="password">Contraseña</label>
          <input
            type="password"
            id="password"
            {...register("password", {
              required: "Campo obligatorio",
              validate: (value) => value.trim() !== "" || "Campo obligatorio",
            })}
          />
          {errors.password && (
            <span role="alert" className={styles["error-message"]}>
              {errors.password.message}
            </span>
          )}
        </div>

        <button className={styles["submit"]} type="submit">
          Ingresar
        </button>
        {/* <p>
          No tienes una cuenta?{" "}
          <a
            href="/signup"
            className={styles["signup-link"]}
            onClick={(e) => {
              e.preventDefault();
              setCurrentPage("signup");
            }}
          >
            Regístrate
          </a>
        </p> */}
      </form>
    </main>
  );
};

export default Login;
