# from fastapi import APIRouter
# from fastapi.responses import JSONResponse

# from app.db import get_db_connection
# from app.models import PaymentRequest
# from app.config import razorpay_client

# router = APIRouter()

# @router.post("/create-order")
# async def create_order(request: PaymentRequest):
#     conn = None
#     cursor = None

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Stored Procedure Call
#         cursor.execute("""
#             EXEC school_management.CreatePaymentOrder
#                 @name=?, 
#                 @email=?, 
#                 @address=?, 
#                 @amount=?
#         """, (request.name, request.email, request.address, request.amount))

#         row = cursor.fetchone()
#         invoice_id = row[0] if row else None

#         if not invoice_id:
#             return JSONResponse(status_code=400, content={"success": False, "message": "Invoice not created"})

#         # Razorpay Order
#         order = razorpay_client.order.create({
#             "amount": int(request.amount * 100),
#             "currency": "INR",
#             "receipt": f"rcpt_{invoice_id}",
#             "payment_capture": 1
#         })

#         # Update DB
#         cursor.execute("""
#             UPDATE invoices 
#             SET razorpay_order_id = ? 
#             WHERE id = ?
#         """, (order["id"], invoice_id))

#         conn.commit()

#         return {
#             "success": True,
#             "order_id": order["id"],
#             "amount": order["amount"],
#             "invoice_id": invoice_id
#         }

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()


from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import traceback

from app.db import get_db_connection
from app.models import PaymentRequest
from app.config import razorpay_client

router = APIRouter()


# -----------------------------
# Payment Verification Model
# -----------------------------
class VerifyPayment(BaseModel):
    invoice_id: int
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str


# -----------------------------
# Create Order
# -----------------------------
@router.post("/create-order")
async def create_order(request: PaymentRequest):

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            EXEC school_management.CreatePaymentOrder
                @name=?,
                @email=?,
                @address=?,
                @amount=?
        """,
        (
            request.name,
            request.email,
            request.address,
            request.amount
        ))

        row = cursor.fetchone()

        if not row:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "Invoice not created"
                }
            )

        invoice_id = row[0]

        # Razorpay Order
        order = razorpay_client.order.create({
            "amount": int(float(request.amount) * 100),
            "currency": "INR",
            "receipt": f"INV_{invoice_id}"
        })

        cursor.execute("""
            UPDATE school_management.invoices
            SET razorpay_order_id=?
            WHERE id=?
        """,
        (
            order["id"],
            invoice_id
        ))

        conn.commit()

        return {
            "success": True,
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "invoice_id": invoice_id
        }

    except Exception as e:

        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# -----------------------------
# Verify Payment
# -----------------------------
@router.post("/verify-payment")
async def verify_payment(data: VerifyPayment):

    conn = None
    cursor = None

    try:

        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": data.razorpay_order_id,
            "razorpay_payment_id": data.razorpay_payment_id,
            "razorpay_signature": data.razorpay_signature
        })

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE school_management.invoices
            SET
                status='paid'
            WHERE
                id=?
        """,
        (
            data.invoice_id,
        ))

        conn.commit()

        return {
            "success": True,
            "message": "Payment Verified"
        }

    except Exception as e:

        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()