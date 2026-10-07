import styles from "./Footer.module.css";
import Logo from "../Logo/Logo";

const Footer = ({ setCurrentPage }) => {
  return (
    <footer className={styles["footer"]}>
      <div className={styles["footer-content"]}>
        <div className={styles["footer-brand"]}>
          <Logo className={styles["logo"]} setCurrentPage={setCurrentPage} />
          <span className={styles["brand-name"]}>PawStore</span>
        </div>

        <div className={styles["social-links"]}>
          <a href="#instagram" onClick={(e) => e.preventDefault()}>
            Instagram
          </a>
          <a href="#facebook" onClick={(e) => e.preventDefault()}>
            Facebook
          </a>
        </div>
      </div>

      <div className={styles["footer-bottom"]}>
        <p className={styles["footer-text"]}>
          © PawStore 2025 — Todos los derechos reservados.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
