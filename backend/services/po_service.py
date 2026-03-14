def calculate_total(items_with_prices: list[dict]) -> tuple[float, float, float]:
    """
    Business logic to calculate total PO amount.
    Accepts: list of dicts with 'quantity' and 'price' (extracted from DB).
    Returns: subtotal, tax(5%), total
    """
    subtotal = sum(item['price'] * item['quantity'] for item in items_with_prices)
    tax = subtotal * 0.05
    total = subtotal + tax
    return round(subtotal, 2), round(tax, 2), round(total, 2)
