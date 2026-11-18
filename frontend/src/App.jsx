import { Navigate, Outlet, Route, Routes } from "react-router-dom";
import Home from "./pages/Home/Home.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";
import Footer from "./components/Footer/Footer.jsx";
import Products from "./pages/Products/Products.jsx";
import ProductDetail from "./pages/ProductDetail/ProductDetail.jsx";
import AdminProducts from "./pages/admin/AdminProducts/AdminProducts.jsx";
import AdminEditProducts from "./pages/admin/AdminEditProducts/AdminEditProducts.jsx";
import "./App.css";
import Login from "./pages/Login/Login.jsx";
import { useAuth } from "./context/AuthContext.jsx";
import errorStyle from "./utils/errorSections.module.css";
import NotFound from "./pages/NotFound/NotFound.jsx";
import Contact from "./pages/contact/Contact.jsx";
import Cart from "./pages/Cart/Cart.jsx";
import Checkout from "./pages/Checkout/Checkout.jsx";
import OrderConfirmed from "./pages/OrderConfirmed/OrderConfirmed.jsx";

const AdminRoute = () => {
  const { user } = useAuth();
  const roles = user?.user?.roles ?? [];
  const isAdmin = roles.some((role) => role.name === "admin");

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!isAdmin) {
    return (
      <div className={errorStyle["error-section"]}>
        <span>No tienes permisos para acceder a esta página</span>
      </div>
    );
  }

  return <Outlet />;
};

const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/productos" element={<Products />} />
        <Route path="/productos/:id" element={<ProductDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/contacto" element={<Contact />} />
        <Route path="/carrito" element={<Cart />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/order-confirmed" element={<OrderConfirmed />} />
        <Route element={<AdminRoute />}>
          <Route path="/admin" element={<AdminProducts />} />
          <Route path="/admin/editar/:id" element={<AdminEditProducts />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
      <Footer />
    </>
  );
};

export default App;
