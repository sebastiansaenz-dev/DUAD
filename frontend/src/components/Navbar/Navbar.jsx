import { NavLink, useNavigate } from "react-router-dom";
import styles from "./Navbar.module.css";
import Logo from "../Logo/Logo";
import CartIcon from "../CartIcon/CartIcon";
import { useAuth } from "../../context/AuthContext.jsx";
import { useCart } from "../../context/CartContext.jsx";
import { logoutRequest } from "../../api/usersApi";

const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { itemCount } = useCart();
  const roles = user?.user?.roles ?? [];
  const isAdmin = roles.some((role) => role.name === "admin");

  const handleLogout = () => {
    logoutRequest()
      .then(() => {
        logout();
        navigate("/");
      })
      .catch(() => {
        logout();
        navigate("/");
      });
  };

  const navItems = [
    { to: "/", label: "Inicio", end: true },
    { to: "/productos", label: "Productos" },
    ...(isAdmin ? [{ to: "/admin", label: "Administración" }] : []),
    { to: "/contacto", label: "Contacto", end: true },
  ];

  return (
    <nav id="navbar" className={styles["navbar"]}>
      <div className={styles["logo-section"]}>
        <Logo className={styles["logo"]} />
        <span>PawStore</span>
      </div>
      <ul className={styles["nav-links"]}>
        {navItems.map((item) => (
          <li key={item.to} className={styles["nav-link"]}>
            <NavLink
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                isActive ? styles["active"] : undefined
              }
            >
              {item.label}
            </NavLink>
          </li>
        ))}
      </ul>
      <div className={styles["login-logout-button-container"]}>
        <div className={styles["cart-logo-container"]}>
          <NavLink
            to="/carrito"
            className={({ isActive }) =>
              isActive
                ? `${styles["cart-link"]} ${styles["cart-link-active"]}`
                : styles["cart-link"]
            }
          >
            <span className={styles["cart-icon-wrap"]}>
              <CartIcon />
              <span className={styles["cart-badge"]}>{itemCount}</span>
            </span>
            <span className={styles["cart-label"]}>Carrito</span>
          </NavLink>
        </div>
        {user && (
          <span className={styles["session-user"]}>
            <span className={styles["session-label"]}>
              Sesión iniciada como
            </span>
            <span className={styles["session-name"]}>
              {user?.user?.username}
            </span>
          </span>
        )}
        <button
          onClick={user ? handleLogout : () => navigate("/login")}
          className={styles["login-logout-button"]}
        >
          {user ? "Cerrar sesión" : "Iniciar sesión"}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
