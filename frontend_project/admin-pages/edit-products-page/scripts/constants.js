export const LOW_STOCK_THRESHOLD = 5;
export const SEARCH_DEBOUNCE_MS = 350;
export const SKU_PATTERN = /^[0-9A-F]{10}$/i;

export const isLikelySku = (term) => SKU_PATTERN.test(term.trim());
