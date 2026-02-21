


BEGIN TRANSACTION;

IF NOT EXISTS(
	SELECT 1
	FROM transactions_exercises."Receipts"
	WHERE id = 7
) THEN
	RETURN;
END IF;


UPDATE transactions_exercises."Products" SET stock = stock + 3 WHERE id = 1;
UPDATE transactions_exercises."Receipts" SET status_id = 2 WHERE id = 7;

COMMIT;


