import styles from "./styles/NotFound.module.css";
import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <>
      <h1 className={styles["not-found-title"]}>Página no encontrada</h1>
      <p className={styles["not-found-message"]}>
        La página que estás buscando no existe o ha sido movida.
      </p>
      <Link
        to="/"
        id="go-to-home-button"
        className={styles["go-back-button"]}
      >
        Volver al inicio
      </Link>
    </>
  );
};

export default NotFound;
