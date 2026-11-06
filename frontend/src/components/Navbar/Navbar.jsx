import styles from "./Navbar.module.css";
import Logo from "../Logo/Logo";
import { useAuthStore } from "../../store/useAuthStore";
import { logoutRequest } from "../../api/usersApi";

const Navbar = ({ currentPage, setCurrentPage }) => {
  const user = useAuthStore((state) => state.user);
  const logoutUser = useAuthStore((state) => state.logout);
  const roles = user?.user?.roles || user?.roles || [];
  const isAdmin = roles.some((role) => role.name === "admin");

  const handleLogout = () => {
    logoutRequest()
      .then(() => {
        logoutUser();
        setCurrentPage("home");
      })
      .catch(() => {
        logoutUser();
        setCurrentPage("home");
      });
  };

  const navItems = [
    { key: "home", label: "Inicio", href: "#home" },
    { key: "products", label: "Productos", href: "#products" },
    { key: "contact", label: "Contacto", href: "#contact" },
    ...(isAdmin
      ? [
          {
            key: "administration",
            label: "Administración",
            href: "#administration",
          },
        ]
      : []),
  ];

  return (
    <nav id="navbar" className={styles["navbar"]}>
      <div className={styles["logo-section"]}>
        <Logo className={styles["logo"]} setCurrentPage={setCurrentPage} />
        <span>PawStore</span>
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
      <div className={styles["login-logout-button-container"]}>
        {user && (
          <span className={styles["session-user"]}>
            <span className={styles["session-label"]}>Sesión iniciada como</span>
            <span className={styles["session-name"]}>
              {user?.user?.username}
            </span>
          </span>
        )}
        <button
          onClick={user ? handleLogout : () => setCurrentPage("login")}
          className={styles["login-logout-button"]}
        >
          {user ? "Cerrar sesión" : "Iniciar sesión"}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
