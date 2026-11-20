import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

let currentUser = null;
let setUserHandler = () => {};

const readStoredUser = () => {
  try {
    return JSON.parse(localStorage.getItem("user"));
  } catch {
    return null;
  }
};

export const getAuthUser = () => currentUser;

export const setAuthUser = (userData) => {
  currentUser = userData;

  if (userData) {
    localStorage.setItem("user", JSON.stringify(userData));
  } else {
    localStorage.removeItem("user");
  }

  setUserHandler(userData);
};

export const runLogout = () => {
  setAuthUser(null);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const storedUser = readStoredUser();
    currentUser = storedUser;
    return storedUser;
  });

  setUserHandler = setUser;

  const login = (userData) => {
    setAuthUser(userData);
  };

  const logout = () => {
    setAuthUser(null);
  };

  const value = { user, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
