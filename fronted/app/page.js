


"use client";

import { useState } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  Spinner,
} from "react-bootstrap";
import {
  FaUser,
  FaEnvelope,
  FaPhoneAlt,
  FaMapMarkerAlt,
  FaRupeeSign,
  FaShieldAlt,
  FaLock,
  FaCheckCircle,
  FaCreditCard,
} from "react-icons/fa";
import { ToastContainer } from "react-toastify";
import {
  Badge,
  Alert,
  InputGroup,
} from "react-bootstrap";
import api from "../services/api";
import { toast } from "react-toastify";

export default function PaymentForm() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    address: "",
    amount: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  // Razorpay script loader
  const loadScript = () => {
    return new Promise((resolve) => {
      const script = document.createElement("script");
      script.src = "https://checkout.razorpay.com/v1/checkout.js";
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  const handleSubmit = async (e) => {

    e.preventDefault();
    setLoading(true);
    console.log("Razorpay Key:", process.env.NEXT_PUBLIC_RAZORPAY_KEY);
    // console.log("Backend Response:", order);

    const res = await loadScript();
    if (!res) {
      alert("Razorpay SDK load failed");
      setLoading(false);
      return;
    }

    try {
      // create order
      const { data: order } = await api.post("/create-order", {
        name: form.name,
        email: form.email,
        address: form.address,
        amount: form.amount,
      });

      const options = {
        key: process.env.NEXT_PUBLIC_RAZORPAY_KEY,
        amount: order.amount,
        currency: order.currency,
        order_id: order.id,

        name: "My Payment System",
        description: "Secure Payment Checkout",

        prefill: {
          name: form.name,
          email: form.email,
          contact: form.phone,
        },

        theme: {
          color: "#198754",
        },

        handler: async function (response) {
          await api.post("/verify-payment", {
            invoice_id: order.invoice_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_order_id: response.razorpay_order_id,
            razorpay_signature: response.razorpay_signature,
          });



          toast.success("🎉 Payment Successful!");
          setLoading(false);
        },
      };

      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (err) {
      console.log(err);
      setLoading(false);
    }
  };

  return (


    <Container
      fluid
      className="d-flex justify-content-center align-items-center py-5"
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb,#0ea5e9)",
      }}
    >
      <ToastContainer
        position="top-right" />

      <Row className="w-100 justify-content-center">
        <Col lg={6} xl={5}>

          <Card
            className="border-0 shadow-lg rounded-5 overflow-hidden"
            style={{
              background: "rgba(255,255,255,0.97)",
              backdropFilter: "blur(20px)",
            }}
          >

            {/* Header */}
            <Card.Header
              className="text-center text-white border-0 py-4"
              style={{
                background:
                  "linear-gradient(90deg,#2563eb,#4f46e5)",
              }}
            >
              <FaCreditCard size={40} />

              <h2 className="fw-bold mt-3 mb-1">
                Secure Payment
              </h2>

              <p className="mb-0 opacity-75">
                Fast • Safe • Trusted
              </p>
            </Card.Header>

            <Card.Body className="p-5">

              <div className="text-center mb-4">



              </div>

              <Form onSubmit={handleSubmit}>

                {/* Name */}

                <InputGroup className="mb-4">

                  <InputGroup.Text>
                    <FaUser />
                  </InputGroup.Text>

                  <Form.Control
                    size="lg"
                    name="name"
                    placeholder="Full Name"
                    value={form.name}
                    onChange={handleChange}
                    required
                  />

                </InputGroup>

                {/* Email */}

                <InputGroup className="mb-4">

                  <InputGroup.Text>
                    <FaEnvelope />
                  </InputGroup.Text>

                  <Form.Control
                    type="email"
                    size="lg"
                    name="email"
                    placeholder="Email Address"
                    value={form.email}
                    onChange={handleChange}
                    required
                  />

                </InputGroup>

                {/* Phone */}

                <InputGroup className="mb-4">

                  <InputGroup.Text>
                    <FaPhoneAlt />
                  </InputGroup.Text>

                  <Form.Control
                    size="lg"
                    name="phone"
                    placeholder="Phone Number"
                    value={form.phone}
                    onChange={handleChange}
                    required
                  />

                </InputGroup>

                {/* Address */}

                <InputGroup className="mb-4">

                  <InputGroup.Text>
                    <FaMapMarkerAlt />
                  </InputGroup.Text>

                  <Form.Control
                    as="textarea"
                    rows={2}
                    name="address"
                    placeholder="Address"
                    value={form.address}
                    onChange={handleChange}
                  />

                </InputGroup>

                {/* Amount */}

                <InputGroup className="mb-3">

                  <InputGroup.Text>
                    <FaRupeeSign />
                  </InputGroup.Text>

                  <Form.Control
                    type="number"
                    size="lg"
                    name="amount"
                    placeholder="Payment Amount"
                    value={form.amount}
                    onChange={handleChange}
                    required
                  />

                </InputGroup>

                {form.amount && (

                  <Alert
                    variant="primary"
                    className="text-center rounded-4"
                  >

                    <strong>
                      Total Amount :
                    </strong>

                    ₹ {form.amount}

                  </Alert>

                )}

                <Button
                  type="submit"
                  size="lg"
                  className="w-100 rounded-pill fw-bold shadow"
                  disabled={loading}
                  style={{
                    background:
                      "linear-gradient(90deg,#16a34a,#22c55e)",
                    border: "none",
                    padding: "15px",
                    fontSize: "18px",
                  }}
                >

                  {loading ? (
                    <>
                      <Spinner
                        animation="border"
                        size="sm"
                        className="me-2"
                      />
                      Processing Payment...
                    </>
                  ) : (
                    <>
                      <FaLock className="me-2" />
                      Pay Securely
                    </>
                  )}

                </Button>

              </Form>

              <hr className="my-4" />

              <Row className="text-center">

                <Col>

                  <FaCheckCircle
                    className="text-success mb-2"
                    size={22}
                  />

                  <div className="small fw-semibold">
                    Secure
                  </div>

                </Col>

                <Col>

                  <FaShieldAlt
                    className="text-primary mb-2"
                    size={22}
                  />

                  <div className="small fw-semibold">
                    Encrypted
                  </div>

                </Col>

                <Col>

                  <FaCreditCard
                    className="text-warning mb-2"
                    size={22}
                  />

                  <div className="small fw-semibold">
                    Razorpay
                  </div>

                </Col>

              </Row>

            </Card.Body>

          </Card>

        </Col>
      </Row>
    </Container>
  );

}