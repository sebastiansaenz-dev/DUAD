export const getEl = (id) => document.getElementById(id);

export const formatPrice = (amount) => {
  return (
    "$" + Number(amount).toLocaleString("en-US", { maximumFractionDigits: 0 })
  );
};

export const escapeHtml = (text) => {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
};

export const showToast = (message) => {
  const toast = getEl("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timeoutId);
  showToast.timeoutId = setTimeout(() => toast.classList.remove("show"), 2200);
};

export const formatDate = (isoString) => {
  const date = new Date(isoString);
  if (isNaN(date.getTime())) return isoString || "—";
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

export const statusToClassName = (status) => {
  return (status || "unknown").toLowerCase().trim().replace(/\s+/g, "-");
};
