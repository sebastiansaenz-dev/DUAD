# 🚀 Cache Strategy

This document details the implementation of optimization layers using Redis to improve the latency and reduce database load

## 🎯 Optimized Endpoints

- **`GET /products`**: As the highest-traffic endpoint, caching this list prevents redundant database queries and reduces the CPU overhead required for model serialization on every request

- **`GET /products/<id>`**: Enables near-instant responses for specific product detail views

- **`GET /carts`**: Caches the active user's shopping cart contents and total calculations to provide fast, responsive loading times for cart and checkout summary pages.

## ⏳ TTL (Time To Live)

| Data type                | TTL (Seconds) | Justification                                                                                                                      |
| :----------------------- | :------------ | :--------------------------------------------------------------------------------------------------------------------------------- |
| **General Product List** | 600 (10 min)  | Balances catalog freshness with server resource optimization.                                                                      |
| **Product Details**      | 3600 (1 h)    | Individual item data changes less frequently then global stock or availability.                                                    |
| **Filtered Lists**       | 300 (5 min)   | Optimizes performance for common search patterns (name, price, brand) with a shorter window to ensure query accuracy.              |
| **Carts**                | 1800 (30 min) | Speeds up cart and checkout loading for authenticated users. Paired with strict proactive invalidation to guarantee data accuracy. |

## 🛠️ Invalidation Strategy

To guarantee **data consistency**, the cache is proactively cleared in the following scenarios:

1. **Automatic Write Invalidation:** Whenever a `POST` request is sent to `/staff-portal/products`, or a `PATCH`/`DELETE` request is executed on `/staff-portal/products/<id>`, a logic is triggered to purge all related Redis keys.

2. **Stock Consistency:** Upon a successful order creation (`POST /orders`), the cache for the involved products is invalidated. This ensures that the updated stock levels are accurately reflected in the very next user query.

3. **Cart Mutations & Checkout:** Whenever a user modifies their cart (adding products, updating quantities, or deleting items) or successfully places an order, the specific user's cache key (`cart:user:{user_id}`) is immediately purged (`delete_data`), forcing a fresh database lookup and calculation on the next request.
