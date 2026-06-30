from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.db import get_db_connection
from app.models import PaymentRequest
from app.config import razorpay_client

router = APIRouter()

@router.post("/create-order")
async def create_order(request: PaymentRequest):
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Stored Procedure Call
        cursor.execute("""
            EXEC CreatePaymentOrder 
                @name=?, 
                @email=?, 
                @address=?, 
                @amount=?
        """, (request.name, request.email, request.address, request.amount))

        row = cursor.fetchone()
        invoice_id = row[0] if row else None

        if not invoice_id:
            return JSONResponse(status_code=400, content={"success": False, "message": "Invoice not created"})

        # Razorpay Order
        order = razorpay_client.order.create({
            "amount": int(request.amount * 100),
            "currency": "INR",
            "receipt": f"rcpt_{invoice_id}",
            "payment_capture": 1
        })

        # Update DB
        cursor.execute("""
            UPDATE invoices 
            SET razorpay_order_id = ? 
            WHERE id = ?
        """, (order["id"], invoice_id))

        conn.commit()

        return {
            "success": True,
            "order_id": order["id"],
            "amount": order["amount"],
            "invoice_id": invoice_id
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()