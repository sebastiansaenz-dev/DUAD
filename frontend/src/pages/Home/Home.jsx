import styles from "./Home.module.css";

const Home = ({ setCurrentPage }) => {
  return (
    <main>
      <div className={styles["welcome-section"]}>
        <div className={styles["welcome-text"]}>
          <h1>Welcome to PawStore</h1>
          <p>
            Everything your best friend needs to live a happy, healthy life.
            Discover premium products designed with love for pets of all kinds.
          </p>
        </div>
        <a>
          <button
            onClick={(e) => {
              e.preventDefault();
              setCurrentPage("products");
            }}
          >
            View products
          </button>
        </a>
      </div>
    </main>
  );
};

export default Home;
