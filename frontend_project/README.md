# PawStore — Frontend

Web interface for the **PawStore** e-commerce platform. It is a static application built with **HTML, CSS, and vanilla JavaScript (ES Modules)** that consumes the Flask REST API.

## Technologies

| Technology | Purpose |
| :--- | :--- |
| **HTML / CSS** | Page structure and styling |
| **JavaScript (ES Modules)** | Per-page logic |
| **Axios** (CDN) | HTTP requests to the backend |
| **Live Server** (recommended) | Local development server |

## Prerequisites

The **backend must be running** before starting the frontend. Without it, all API requests will fail.

| Requirement | Details |
| :--- | :--- |
| **Backend running** | API available at `http://localhost:5002` |
| **PostgreSQL** | Database configured and migrated |
| **Redis** | Backend cache (optional in dev, but recommended) |
| **Live Server** | VS Code extension or any static server on port **5500** |

> **Important:** Pages use `type="module"`. They will not work when opened directly via `file://`. You must serve the folder with a local server.

## Getting Started

### 1. Start the backend (required first)

Follow the instructions in the backend README:

```bash
cd backend_project
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
cp .env.example .env        # Configure DATABASE_URL, SECRET_KEY, Redis, etc.
flask db upgrade
python app.py
```

The API will be available at:

```
http://localhost:5002
```

### 2. Start the frontend

1. Open the `frontend_project` folder in VS Code.
2. Install the **Live Server** extension (if you don't have it).
3. Right-click any `.html` file (e.g. `landing-page/home.html`) → **Open with Live Server**.

The frontend will be served at:

```
http://127.0.0.1:5500
```

> The backend has CORS configured for `http://127.0.0.1:5500` and `http://localhost:5500`. Use one of those origins.

### 3. Entry point

Open in your browser:

```
http://127.0.0.1:5500/landing-page/home.html
```

---

## Project Structure

```
frontend_project/
├── landing-page/              # Home page
├── product-catalog-page/      # Product catalog (pagination + search)
├── single-product-page/       # Product detail + add to cart
├── cart-page/                 # View and remove cart items
├── order-summary-page/        # Order summary + shipping form
├── order-confirmed-page/      # Order confirmation
├── login-page/                # Login
├── signup-page/               # User registration
├── user-page/                 # Client profile
├── admin-pages/               # Admin panel
│   ├── edit-products-page/    # Product CRUD
│   ├── orders-page/           # Order management
│   └── users-page/            # User management
├── utils/                     # Shared utilities (API, auth, navbar)
└── svgs/                      # SVG icons
```

Each page follows the same pattern:

```
page-name/
├── page.html          # Static HTML
├── scripts/           # JS logic (api.js, render.js, main/init)
└── styles/            # Modular CSS per section
```

---

## Backend Connection

### API Configuration

All backend communication goes through `utils/utils.js`:

```javascript
export const api = axios.create({
  baseURL: "http://localhost:5002",
});
```

- **`api`**: Authenticated requests (JWT attached automatically).
- **`apiPublic`**: Public requests (login, register, product listing).

### Endpoints Used

#### Public (no authentication)

| Action | Method | Endpoint | Page |
| :--- | :--- | :--- | :--- |
| List products | `GET` | `/products/?page=&name=` | Catalog |
| Login | `POST` | `/users/login` | Login |
| Register | `POST` | `/users/register-user` | Signup |

#### Protected (JWT required)

| Action | Method | Endpoint | Page |
| :--- | :--- | :--- | :--- |
| Product detail | `GET` | `/products/:id` | Single product |
| View cart | `GET` | `/cart/` | Cart, Order summary |
| Add to cart | `POST` | `/cart/` | Single product |
| Remove from cart | `DELETE` | `/cart/` | Cart |
| Create order | `POST` | `/orders/` | Order summary |
| List my orders | `GET` | `/orders/` | — |
| Refresh token | `POST` | `/refresh/` | Automatic (interceptor) |

#### Admin (requires `admin` role)

| Action | Method | Endpoint | Page |
| :--- | :--- | :--- | :--- |
| Product CRUD | `GET/POST/PATCH/DELETE` | `/staff-portal/products/` | Edit products |
| Update order | `PATCH` | `/staff-portal/orders/:id` | Orders |
| Manage users | `GET/PATCH/DELETE` | `/staff-portal/users/` | Users |

---

## Authentication

### Login / Register Flow

1. The user submits credentials to `/users/login` or `/users/register-user`.
2. The backend responds with `access_token`, `refresh_token`, and `user` data.
3. The frontend stores everything in **`localStorage`** under the key `"user"`:

```json
{
  "user": { "id": 1, "email": "...", "username": "...", "roles": [...] },
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

### Axios Interceptor

- Every `api` request attaches `Authorization: Bearer <access_token>`.
- If the backend returns **401**, the token is refreshed via `POST /refresh/`.
- If the refresh token is also expired, `localStorage` is cleared and the user is redirected to login.

### Protected Routes

| Type | Behavior |
| :--- | :--- |
| **Client** (cart, checkout, profile) | Redirects to login if there is no session |
| **Admin** (`protectAdminRoute()`) | Redirects to login or home if the user does not have the `admin` role |

---

## Purchase Flow (Client)

```
Landing → Catalog → Product detail → Cart → Order summary → Order confirmed
```

### Step by Step

1. **Catalog** (`product-catalog-page`): loads products with `GET /products/`. Supports pagination and search by name.
2. **Product detail** (`single-product-page`): displays a product via `GET /products/:id`. Clicking "Add to cart" sends `POST /cart/` with `[{ id, quantity }]`. Requires login.
3. **Cart** (`cart-page`): fetches the cart with `GET /cart/`. Allows removing items with `DELETE /cart/`. The cart lives on the **backend** (PostgreSQL + Redis cache), not in the browser.
4. **Order summary** (`order-summary-page`): reloads the cart, shows the total and a form (name, address, phone). On submit, sends `POST /orders/`.
5. **Order confirmed** (`order-confirmed-page`): reads order data from **`sessionStorage`** (`lastOrder`), displays it, then removes it. The cart is cleared on the backend when the order is created.

```
┌─────────────┐    GET /cart/     ┌──────────────┐    POST /orders/    ┌──────────────────┐
│  Cart page  │ ───────────────►  │ Order summary│ ─────────────────►  │ Order confirmed  │
└─────────────┘                   └──────────────┘                     └──────────────────┘
                                         │                                      ▲
                                         │ sessionStorage.setItem("lastOrder")  │
                                         └──────────────────────────────────────┘
```

---

## Admin Panel

Accessible only to users with the **`admin`** role. The navbar shows the "Admin Panel" link automatically.

| Section | Route | Functionality |
| :--- | :--- | :--- |
| Products | `admin-pages/edit-products-page/products.html` | Create, edit, delete, and search products |
| Orders | `admin-pages/orders-page/orders.html` | View orders and update their status |
| Users | `admin-pages/users-page/users.html` | View, edit, and delete users |

---

## Shared Utilities (`utils/utils.js`)

| Function | Description |
| :--- | :--- |
| `checkAuth()` | Reads and parses the user from `localStorage` |
| `showUserType()` | Renders the dynamic navbar (login, cart, logout, admin/profile links) |
| `activePage()` | Highlights the active page in navigation |
| `showErrorMessage(error)` | Displays backend errors in `#error-section` |
| `logout()` | Clears the session and redirects to login |
| `protectAdminRoute()` | Guard for admin routes |

---

## Browser Storage

| Storage | Key | Content | Duration |
| :--- | :--- | :--- | :--- |
| `localStorage` | `"user"` | JWT tokens + user data | Until logout or refresh token expiry (7 days) |
| `sessionStorage` | `"lastOrder"` | Snapshot of the newly created order | Only during redirect to the confirmation page |

> The cart is **not** stored in the browser. It is always fetched from the backend via `GET /cart/`.

---

## Troubleshooting

| Problem | Likely cause | Solution |
| :--- | :--- | :--- |
| CORS error in console | Backend not running or frontend not on port 5500 | Start the backend and use Live Server |
| `Failed to fetch module` | HTML opened via `file://` | Use Live Server |
| Constant redirect to login | Expired token or backend restarted | Log in again |
| Cart shows old items after purchase | Stale Redis cache | Restart Redis or wait for expiry (backend invalidates cache on order creation) |
| Confirmation page redirects to catalog | No `lastOrder` in sessionStorage | Complete checkout from the order summary page; do not navigate directly to the URL |

---

## Development Notes

- To change the backend URL, edit `baseURL` in `utils/utils.js`.
- Axios is loaded from CDN in each `.html` file; there is no `package.json` or bundler.
- Styles are organized by component/section inside each `styles/` folder.
- For more API details, see the [backend README](../backend_project/README.md).
