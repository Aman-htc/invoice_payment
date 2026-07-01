# # import os
# # from dotenv import load_dotenv
# # import razorpay

# # load_dotenv()

# # razorpay_client = razorpay.Client(
# #     auth=(
# #         os.getenv("RAZORPAY_KEY_ID"),
# #         os.getenv("RAZORPAY_KEY_SECRET")
# #     )
# # )

# # RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")

# import os
# from dotenv import load_dotenv
# import razorpay

# load_dotenv()

# print("KEY_ID =", os.getenv("RAZORPAY_KEY_ID"))
# print("KEY_SECRET =", os.getenv("RAZORPAY_KEY_SECRET"))

# razorpay_client = razorpay.Client(
#     auth=(
#         os.getenv("RAZORPAY_KEY_ID"),
#         os.getenv("RAZORPAY_KEY_SECRET")
#     )
# )

# RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")import razorpay
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = razorpay.Client(
#     auth=(
#         os.getenv("RAZORPAY_KEY_ID"),
#         os.getenv("RAZORPAY_KEY_SECRET")
#     )
# )

# try:
#     result = client.order.all()
#     print(result)
# except Exception as e:
#     import traceback
#     traceback.print_exc()

import os
from dotenv import load_dotenv
import razorpay

load_dotenv()

print("KEY_ID =", os.getenv("RAZORPAY_KEY_ID"))
print("KEY_SECRET =", os.getenv("RAZORPAY_KEY_SECRET"))

razorpay_client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)

RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")