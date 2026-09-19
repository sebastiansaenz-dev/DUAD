- **`api`**: Authenticated requests (JWT attached automatically).
- **`apiPublic`**: Public requests (login, register, product listing).

### Endpoints Used

#### Public (no authentication)

| Action        | Method | Endpoint                 | Page    |
| :------------ | :----- | :----------------------- | :------ |
| List products | `GET`  | `/products/?page=&name=` | Catalog |
| Login         | `POST` | `/users/login`           | Login   |
| Register      | `POST` | `/users/register-user`   | Signup  |

#### Protected (JWT required)

| Action           | Method   | Endpoint        | Page                    |
| :--------------- | :------- | :-------------- | :---------------------- |
| Product detail   | `GET`    | `/products/:id` | Single product          |
| View cart        | `GET`    | `/cart/`        | Cart, Order summary     |
| Add to cart      | `POST`   | `/cart/`        | Single product          |
| Remove from cart | `DELETE` | `/cart/`        | Cart                    |
| Create order     | `POST`   | `/orders/`      | Order summary           |
| Refresh token    | `POST`   | `/refresh/`     | Automatic (interceptor) |

#### Admin (requires `admin` role)

| Action       | Method                  | Endpoint                   | Page          |
| :----------- | :---------------------- | :------------------------- | :------------ |
| Product CRUD | `GET/POST/PATCH/DELETE` | `/staff-portal/products/`  | Edit products |
| Update order | `PATCH`                 | `/staff-portal/orders/:id` | Orders        |
| Manage users | `GET/PATCH/DELETE`      | `/staff-portal/users/`     | Users         |

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

| Type                                 | Behavior                                                              |
| :----------------------------------- | :-------------------------------------------------------------------- |
| **Client** (cart, checkout, profile) | Redirects to login if there is no session                             |
| **Admin** (`protectAdminRoute()`)    | Redirects to login or home if the user does not have the `admin` role |

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

| Function                  | Description                                                           |
| :------------------------ | :-------------------------------------------------------------------- |
| `checkAuth()`             | Reads and parses the user from `localStorage`                         |
| `showUserType()`          | Renders the dynamic navbar (login, cart, logout, admin/profile links) |
| `activePage()`            | Highlights the active page in navigation                              |
| `showErrorMessage(error)` | Displays backend errors in `#error-section`                           |
| `logout()`                | Clears the session and redirects to login                             |
| `protectAdminRoute()`     | Guard for admin routes                                                |

---

## Browser Storage

| Storage          | Key           | Content                             | Duration                                      |
| :--------------- | :------------ | :---------------------------------- | :-------------------------------------------- |
| `localStorage`   | `"user"`      | JWT tokens + user data              | Until logout or refresh token expiry (7 days) |
| `sessionStorage` | `"lastOrder"` | Snapshot of the newly created order | Only during redirect to the confirmation page |

> The cart is **not** stored in the browser. It is always fetched from the backend via `GET /cart/`.

---

## Troubleshooting

| Problem                                | Likely cause                                     | Solution                                                                           |
| :------------------------------------- | :----------------------------------------------- | :--------------------------------------------------------------------------------- |
| CORS error in console                  | Backend not running or frontend not on port 5500 | Start the backend and use Live Server                                              |
| `Failed to fetch module`               | HTML opened via `file://`                        | Use Live Server                                                                    |
| Constant redirect to login             | Expired token or backend restarted               | Log in again                                                                       |
| Cart shows old items after purchase    | Stale Redis cache                                | Restart Redis or wait for expiry (backend invalidates cache on order creation)     |
| Confirmation page redirects to catalog | No `lastOrder` in sessionStorage                 | Complete checkout from the order summary page; do not navigate directly to the URL |

---

## Development Notes

- To change the backend URL, edit `baseURL` in `utils/utils.js`.
- Axios is loaded from CDN in each `.html` file; there is no `package.json` or bundler.
- Styles are organized by component/section inside each `styles/` folder.
- For more API details, see the [backend README](../backend_project/README.md).
