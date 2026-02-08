



SELECT
	u.username,
	pc.cart_id,
	p.name,
	pc.product_id AS product_id,
	p.price AS unit_price,
	pc.quantity,
	ROUND(p.price * pc.quantity) AS total
FROM lyfter_ecommerce."Users" u
JOIN lyfter_ecommerce."Carts" c
	ON c.user_id = u.id
JOIN lyfter_ecommerce."Products_carts" pc
	ON pc.cart_id = c.id
JOIN lyfter_ecommerce."Products" p
	ON pc.product_id = p.id
WHERE u.id = 22


SELECT
	u.username,
	pm.name AS payment_method,
	s.date,
	p.name AS product_name,
	p.price AS unit_price,
	ps.quantity,
	ROUND(p.price * ps.quantity) AS product_total,
	s.total,
	t.name,
	s.parent_sale_id
FROM lyfter_ecommerce."Users" u
JOIN lyfter_ecommerce."Carts" c
	ON c.user_id = u.id
JOIN lyfter_ecommerce."Sales" s
	ON s.cart_id = c.id
JOIN lyfter_ecommerce."Payment_methods" pm
	ON s.payment_method_id = pm.id
JOIN lyfter_ecommerce."Products_sales" ps
	ON ps.sale_id = s.id
JOIN lyfter_ecommerce."Products" p
	ON ps.product_id = p.id
JOIN lyfter_ecommerce."Sales_type" t
	ON s.type_id = t.id
WHERE u.id = 11


SELECT
	p.name,
	p.price,
	ps.quantity,
	ROUND(p.price * ps.quantity) AS product_total,
	s.total,
	s.date,
	t.name AS payment_method,
	s.parent_sale_id
FROM lyfter_ecommerce."Users" u
JOIN lyfter_ecommerce."Carts" c
	ON c.user_id = u.id
JOIN lyfter_ecommerce."Sales" s
	ON s.cart_id = c.id
JOIN lyfter_ecommerce."Products_sales" ps
	ON ps.sale_id = s.id
JOIN lyfter_ecommerce."Sales_type" t
	ON s.type_id = t.id
JOIN lyfter_ecommerce."Products" p
	ON ps.product_id = p.id
WHERE s.id = 1
	


SELECT
	u.id,
	u.username,
	SUM(s.total) as total
FROM lyfter_ecommerce."Users" u
JOIN lyfter_ecommerce."Carts" c
	ON c.user_id = u.id
JOIN lyfter_ecommerce."Sales" s
	ON s.cart_id = c.id
GROUP BY u.id
ORDER BY total DESC
LIMIT 3




