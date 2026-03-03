"""
Test Fixture: Excessive Parameters Vulnerable Pattern (Python)

This file contains functions with >5 parameters.
Expected detections: >=2 violations for AP-008
Rule ID: AP-008
Severity: MEDIUM (info)
"""


def create_user(
    user_id,
    username,
    email,
    password,
    first_name,
    last_name,
    phone_number,
):
    """VULNERABLE: 7 parameters - too many."""
    return {
        "id": user_id,
        "username": username,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone_number,
    }


def process_order(
    order_id,
    customer_id,
    product_id,
    quantity,
    price,
    discount,
    tax_rate,
    shipping_method,
):
    """VULNERABLE: 8 parameters - too many."""
    subtotal = quantity * price
    discount_amount = subtotal * discount
    tax_amount = (subtotal - discount_amount) * tax_rate
    return {
        "order_id": order_id,
        "total": subtotal - discount_amount + tax_amount,
    }


def acceptable_function(a, b, c, d, e):
    """SAFE: 5 parameters is acceptable."""
    return a + b + c + d + e
