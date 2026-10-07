# PawStore - Frontend (React)

Web app for the **PawStore** shop, built with **React** and **Vite**. This is **Stage 1**: navigation between views (Home, Catalog, and Product detail) and product data loaded from a local JSON file (`data/products.json`).

## Requirements

- [Node.js](https://nodejs.org/) **18 or later** (**20+** recommended)
- npm (included with Node.js)

## Install dependencies

```bash
npm install

```

## Development

Start the Vite dev server:

```bash
npm run dev
```

Open in your browser the URL shown in the terminal (default: http://localhost:5173)

## Proyect layout

frontend/
├── data/products.json # Product data (JSON)
├── public/ # Static assets
└── src/
├── components/ # Navbar, Footer, ProductCard, Logo
├── pages/ # Home, Products, ProductDetail
├── App.jsx # View switching via component state
└── main.jsx # React entry point
