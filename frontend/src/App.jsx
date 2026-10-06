import { useState } from "react";
import Home from "./pages/Home/Home.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";
import Footer from "./components/Footer/Footer.jsx";
import Products from "./pages/Products/Products.jsx";
import ProductDetail from "./pages/ProductDetail/ProductDetail.jsx";
import "./App.css";

const App = () => {
  const [currentPage, setCurrentPage] = useState("home");
  const [selectedProduct, setSelectedProduct] = useState(null);
  return (
    <>
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      {currentPage === "home" && <Home setCurrentPage={setCurrentPage} />}
      {currentPage === "products" && (
        <Products
          setCurrentPage={setCurrentPage}
          setSelectedProduct={setSelectedProduct}
        />
      )}
      {currentPage === "product-detail" && (
        <ProductDetail
          product={selectedProduct}
          setCurrentPage={setCurrentPage}
        />
      )}
      <Footer setCurrentPage={setCurrentPage} />
    </>
  );
};

export default App;
