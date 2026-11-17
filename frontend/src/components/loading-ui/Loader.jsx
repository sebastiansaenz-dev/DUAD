import styles from "./Spinner.module.css";

const Loader = () => {
  return (
    <div>
      <span className={styles["loader"]}></span>
    </div>
  );
};

export default Loader;
