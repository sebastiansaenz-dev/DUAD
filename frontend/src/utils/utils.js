export const isActiveRoute = (currentPath, href) => {
  if (!href || href === "#") return false;
  const currentFileName = currentPath.split("/").pop() || "home.html";
  const targetFileName = href.split("/").pop();
  return currentFileName === targetFileName;
};
