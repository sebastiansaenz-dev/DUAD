import styles from "./Navbar.module.css";
import Logo from "../Logo/Logo";

const Navbar = ({ currentPage, setCurrentPage }) => {
  const navItems = [
    { key: "home", label: "Inicio", href: "#home" },
    { key: "products", label: "Productos", href: "#products" },
    { key: "contact", label: "Contacto", href: "#contact" },
  ];

  return (
    <nav id="navbar" className={styles["navbar"]}>
      <div>
        <Logo className={styles["logo"]} setCurrentPage={setCurrentPage} />
      </div>
      <ul className={styles["nav-links"]}>
        {navItems.map((item) => (
          <li
            key={item.key}
            className={`${styles["nav-link"]} ${currentPage === item.key ? styles["active"] : ""}`}
          >
            <a
              href={item.href}
              onClick={(e) => {
                e.preventDefault();
                setCurrentPage(item.key);
              }}
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
      <div className={styles["cart-logo-container"]}></div>
    </nav>
  );
};

export default Navbar;
