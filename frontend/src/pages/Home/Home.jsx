import { useNavigate } from "react-router-dom";
import styles from "./Home.module.css";

const Home = () => {
  const navigate = useNavigate();
  return (
    <main>
      <div className={styles["welcome-section"]}>
        <div className={styles["welcome-text"]}>
          <h1>Bienvenido a PawStore</h1>
          <p>
            Somos una tienda dedicada a ofrecer productos de calidad para tus
            mascotas.
          </p>
          <br />
          <p>
            Explora nuestro catálogo para encontrar camas, juguetes, accesorios
            y más.
          </p>
        </div>
        <div className={styles["welcome-actions"]}>
          <button
            onClick={() => {
              navigate("/products");
            }}
          >
            View products
          </button>
          <p>
            Esta es la página principal de la aplicación. Más adelante aquí se
            podrán mostrar productos destacados.
          </p>
        </div>
      </div>
    </main>
  );
};

export default Home;
