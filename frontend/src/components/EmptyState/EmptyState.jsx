import { Link } from "react-router-dom";
import styles from "./EmptyState.module.css";

const EmptyState = ({ title, message, actionTo, actionLabel }) => {
  return (
    <div className={styles["empty-state"]}>
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M9 9H9.01"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M15 9H15.01"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M9 16C9 16 10.5 14.5 12 14.5C13.5 14.5 15 16 15 16"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <h2>{title}</h2>
      {message && <p>{message}</p>}
      {actionTo && actionLabel && (
        <Link to={actionTo} className={styles["empty-state-link"]}>
          {actionLabel}
        </Link>
      )}
    </div>
  );
};

export default EmptyState;
