"""
Input validation functions for the trading bot.
Validates all user inputs before sending orders to Binance.
"""
import re


def validate_symbol(symbol: str) -> str:
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading symbol (e.g., BTCUSDT)
    
    Returns:
        Validated symbol (uppercase)
    
    Raises:
        ValueError: If symbol format is invalid
    """
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string")
    
    symbol = symbol.upper().strip()
    
    # Basic validation: alphanumeric, length check
    if not symbol or len(symbol) < 3 or len(symbol) > 20:
        raise ValueError(
            f"Symbol must be between 3 and 20 characters. Received: {symbol}"
        )
    
    if not re.match(r"^[A-Z0-9]+$", symbol):
        raise ValueError(
            f"Symbol must contain only alphanumeric characters. Received: {symbol}"
        )
    
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side (BUY or SELL).
    
    Args:
        side: Order side (BUY or SELL)
    
    Returns:
        Validated side (uppercase)
    
    Raises:
        ValueError: If side is not BUY or SELL
    """
    if not isinstance(side, str):
        raise ValueError("Side must be a string")
    
    side = side.upper().strip()
    
    if side not in ["BUY", "SELL"]:
        raise ValueError(
            f"Side must be 'BUY' or 'SELL'. Received: {side}"
        )
    
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type (MARKET or LIMIT).
    
    Args:
        order_type: Order type (MARKET or LIMIT)
    
    Returns:
        Validated order type (uppercase)
    
    Raises:
        ValueError: If order type is not MARKET or LIMIT
    """
    if not isinstance(order_type, str):
        raise ValueError("Order type must be a string")
    
    order_type = order_type.upper().strip()
    
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError(
            f"Order type must be 'MARKET' or 'LIMIT'. Received: {order_type}"
        )
    
    return order_type


def validate_quantity(quantity: float) -> float:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity (in contracts)
    
    Returns:
        Validated quantity
    
    Raises:
        ValueError: If quantity is not a positive number
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValueError(
            f"Quantity must be a number. Received: {quantity}"
        )
    
    if qty <= 0:
        raise ValueError(
            f"Quantity must be greater than 0. Received: {qty}"
        )
    
    return qty


def validate_price(price: float, order_type: str) -> float:
    """
    Validate order price.
    
    Args:
        price: Order price
        order_type: Order type (MARKET or LIMIT)
    
    Returns:
        Validated price
    
    Raises:
        ValueError: If price is invalid for the order type
    """
    if order_type == "MARKET":
        if price is not None:
            raise ValueError(
                "Price should not be provided for MARKET orders"
            )
        return None
    
    if order_type == "LIMIT":
        if price is None:
            raise ValueError(
                "Price is required for LIMIT orders"
            )
        
        try:
            p = float(price)
        except (ValueError, TypeError):
            raise ValueError(
                f"Price must be a number. Received: {price}"
            )
        
        if p <= 0:
            raise ValueError(
                f"Price must be greater than 0. Received: {p}"
            )
        
        return p
