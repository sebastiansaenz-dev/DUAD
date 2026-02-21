


BEGIN TRANSACTION;

IF NOT EXISTS(
	SELECT 1
	FROM transactions_exercises."Products"
	WHERE id = 1 AND stock >= 3
) THEN 
	RETURN;
END IF;


IF NOT EXISTS(
	SELECT 1
	FROM transactions_exercises."Users"
	WHERE id = 1
) THEN 
	RETURN;
END IF;


INSERT INTO transactions_exercises."Receipts" (user_id, status_id) VALUES (1, 1);

INSERT INTO transactions_exercises."Products_receipts" (product_id, receipt_id, quantity) VALUES (1, 7, 3);

UPDATE transactions_exercises."Products" SET stock = stock - 3 WHERE id = 1;

SAVEPOINT receipt_created;


IF NOT EXISTS(
	SELECT 1
	FROM transactions_exercises."Receipts"
	WHERE id = 7
) THEN
	ROLLBACK receipt_created;
	RETURN;
END IF;

COMMIT;


