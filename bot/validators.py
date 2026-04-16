"""Input validation for trading bot."""

from typing import Optional
import re


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_symbol(symbol: str) -> str:
    """Validate trading symbol.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        
    Returns:
        Uppercase symbol
        
    Raises:
        ValidationError: If symbol format is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    # Symbol should contain only letters and numbers
    if not re.match(r"^[A-Z0-9]+$", symbol.upper()):
        raise ValidationError(f"Invalid symbol format: {symbol}")
    
    # Most Binance futures symbols end with USDT
    symbol = symbol.upper()
    if not symbol.endswith("USDT"):
        raise ValidationError(f"Symbol should end with USDT for futures trading: {symbol}")
    
    return symbol


def validate_side(side: str) -> str:
    """Validate order side.
    
    Args:
        side: Order side (BUY or SELL)
        
    Returns:
        Uppercase side
        
    Raises:
        ValidationError: If side is invalid
    """
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValidationError(f"Invalid side: {side}. Must be BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type.
    
    Args:
        order_type: Order type (MARKET or LIMIT)
        
    Returns:
        Uppercase order type
        
    Raises:
        ValidationError: If order type is invalid
    """
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValidationError(f"Invalid order type: {order_type}. Must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity: float) -> float:
    """Validate order quantity.
    
    Args:
        quantity: Order quantity
        
    Returns:
        Validated quantity
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quantity: {quantity}. Must be a number")
    
    if qty <= 0:
        raise ValidationError(f"Quantity must be positive: {qty}")
    
    return qty


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """Validate order price.
    
    Args:
        price: Order price (required for LIMIT orders)
        order_type: Order type
        
    Returns:
        Validated price or None for MARKET orders
        
    Raises:
        ValidationError: If price is invalid
    """
    if order_type == "MARKET":
        return None
    
    if order_type == "LIMIT" and price is None:
        raise ValidationError("Price is required for LIMIT orders")
    
    try:
        price_val = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid price: {price}. Must be a number")
    
    if price_val <= 0:
        raise ValidationError(f"Price must be positive: {price_val}")
    
    return price_val
