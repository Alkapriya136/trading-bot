"""Order placement logic."""

import logging
from typing import Dict, Any, Optional
from bot.client import BinanceFuturesClient
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    ValidationError
)


class OrderManager:
    """Manages order placement and validation."""
    
    def __init__(self, testnet: bool = True):
        """Initialize order manager.
        
        Args:
            testnet: Whether to use testnet
        """
        self.logger = logging.getLogger("trading_bot.orders")
        self.client = BinanceFuturesClient(testnet=testnet)
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Place an order with validation.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT)
            
        Returns:
            Order response and summary
            
        Raises:
            ValidationError: If input validation fails
            Exception: If order placement fails
        """
        try:
            # Validate inputs
            self.logger.info("Validating order parameters")
            symbol = validate_symbol(symbol)
            side = validate_side(side)
            order_type = validate_order_type(order_type)
            quantity = validate_quantity(quantity)
            price = validate_price(price, order_type)
            
            # Verify symbol exists
            symbol_info = self.client.get_symbol_info(symbol)
            if not symbol_info:
                raise ValidationError(f"Symbol {symbol} not found on Binance Futures")
            
            # Create order summary
            order_summary = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
                "price": price if price else "MARKET"
            }
            
            self.logger.info(f"Order Summary: {order_summary}")
            
            # Place order based on type
            if order_type == "MARKET":
                response = self.client.place_market_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity
                )
            else:  # LIMIT
                response = self.client.place_limit_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    price=price
                )
            
            # Extract key information from response
            order_details = {
                "orderId": response.get("orderId"),
                "symbol": response.get("symbol"),
                "status": response.get("status"),
                "side": response.get("side"),
                "type": response.get("type"),
                "origQty": response.get("origQty"),
                "executedQty": response.get("executedQty", "0"),
                "avgPrice": response.get("avgPrice", "N/A"),
                "price": response.get("price", "MARKET"),
                "timeInForce": response.get("timeInForce", "N/A"),
                "updateTime": response.get("updateTime")
            }
            
            return {
                "success": True,
                "order_summary": order_summary,
                "order_response": order_details,
                "full_response": response
            }
            
        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            return {
                "success": False,
                "error_type": "ValidationError",
                "error_message": str(e)
            }
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            return {
                "success": False,
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
