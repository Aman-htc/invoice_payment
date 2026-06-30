from fastapi import APIRouter, Request, HTTPException
import hmac, hashlib

from app.db import get_db_connection
from app.config import RAZORPAY_WEBHOOK_SECRET

router = APIRouter()

@router.post("/webhook")
async def razorpay_webhook(request: Request):
    try:
        body = await request.body()
        signature = request.headers.get("X-Razorpay-Signature")

        expected_sig = hmac.new(
            RAZORPAY_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        if not signature or not hmac.compare_digest(expected_sig, signature):
            raise HTTPException(status_code=400, detail="Invalid signature")

        payload = await request.json()

        if payload.get("event") == "payment.captured":
            payment = payload["payload"]["payment"]["entity"]
            order_id = payment["order_id"]

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM invoices WHERE razorpay_order_id = ?",
                (order_id,)
            )
            row = cursor.fetchone()

            if row:
                invoice_id = row[0]

                cursor.execute("""
                    UPDATE invoices 
                    SET status = 'paid'
                    WHERE id = ?
                """, (invoice_id,))

                cursor.execute("""
                    INSERT INTO payments 
                    (invoice_id, razorpay_payment_id, status, amount)
                    VALUES (?, ?, 'success', ?)
                """, (
                    invoice_id,
                    payment["id"],
                    payment["amount"] / 100
                ))

                conn.commit()

            cursor.close()
            conn.close()

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "message": str(e)}