import json
import logging
import os
import subprocess
from pathlib import Path

WORKER_DIR = Path(__file__).resolve().parents[1] / "email-worker"


def send_order_confirmation_email(to_email, order):
    if not to_email:
        logging.warning("Order email skipped: no recipient")
        return

    items = []
    for item in order.items or []:
        product = item.product
        quantity = int(item.quantity or 0)
        price = int(item.price_at_purchase or 0)
        items.append(
            {
                "name": getattr(product, "name", None) or "Producto",
                "quantity": quantity,
                "imageUrl": getattr(product, "image_url", None) or "",
                "lineTotal": price * quantity,
            }
        )

    payload = {
        "to": to_email,
        "fullName": order.full_name or "cliente",
        "username": getattr(getattr(order, "user", None), "username", None),
        "email": to_email,
        "phone": order.phone,
        "address": order.address,
        "payment": "Sinpe",
        "orderNumber": order.order_number,
        "total": int(order.total or 0),
        "catalogUrl": "http://localhost:5173/products",
        "items": items,
    }

    try:
        result = subprocess.run(
            ["node", "--import", "tsx", "send.jsx"],
            cwd=WORKER_DIR,
            input=json.dumps(payload).encode("utf-8"),
            capture_output=True,
            timeout=60,
            env=os.environ.copy(),
        )
    except Exception as ex:
        logging.error("Could not start email send: %s", ex)
        return

    if result.returncode != 0:
        error_text = (result.stderr or result.stdout).decode("utf-8", errors="replace")
        logging.error("Order email failed: %s", error_text.strip())
        return

    logging.info((result.stdout or b"").decode("utf-8", errors="replace").strip())
