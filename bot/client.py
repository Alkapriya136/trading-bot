"""Binance Futures API client wrapper."""

import os
import logging
from typing import Dict, Any, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from pathlib import Path


class BinanceFuturesClient:
    """Wrapper for Binance Futures API client."""
    
    def __init__(self, testnet: bool = True):
        """Initialize Binance Futures client.
        
        Args:
            testnet: Whether to use testnet (default: True)
        """
        self.logger = logging.getLogger("trading_bot.client")
        
        # Load environment variables
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(env_path)
        
        # Get API credentials
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.secret_key = os.getenv("BINANCE_SECRET_KEY")
        
        if not self.api_key or not self.secret_key:
            raise ValueError(
                "Binance API credentials not found. "
                "Please set BINANCE_API_KEY and BINANCE_SECRET_KEY in .env file"
            )
        
        # Mask credentials for logging
        masked_key = self.api_key[:8] + "..." + self.api_key[-4:] if len(self.api_key) > 12 else "***"
        self.logger.info(f"Initializing Binance client with API key: {masked_key}")
        
        # Initialize client
        if testnet:
          self.client = Client(
             api_key=self.api_key,
             api_secret=self.secret_key
        )
    # Correct attribute names for futures testnet
          self.client.FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"
          self.client.futures_coin_testnet = True
          self.client.API_URL = "https://testnet.binancefuture.com"
          self.logger.info("Connected to Binance Futures TESTNET")
        # if testnet:
        #     self.client = Client(
        #         api_key=self.api_key,
        #         api_secret=self.secret_key,
        #         testnet=True
        #     )
        #     # Set testnet URL for futures
        #     self.client.FUTURES_URL = "https://testnet.binancefuture.com"
        #     self.logger.info("Connected to Binance Futures TESTNET")
        else:
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.secret_key
            )
            self.logger.info("Connected to Binance Futures LIVE")
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get futures account information.
        
        Returns:
            Account information dictionary
        """
        try:
            self.logger.debug("Fetching account information")
            account_info = self.client.futures_account()
            self.logger.info("Successfully retrieved account information")
            return account_info
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            self.logger.error(f"Binance request error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error getting account info: {e}")
            raise
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get trading pair information.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Symbol information or None if not found
        """
        try:
            self.logger.debug(f"Fetching symbol info for {symbol}")
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info["symbols"]:
                if s["symbol"] == symbol:
                    self.logger.info(f"Found symbol info for {symbol}")
                    return s
            
            self.logger.warning(f"Symbol not found: {symbol}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting symbol info: {e}")
            raise
    
    def place_market_order(
        self, 
        symbol: str, 
        side: str, 
        quantity: float
    ) -> Dict[str, Any]:
        """Place a market order.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY or SELL)
            quantity: Order quantity
            
        Returns:
            Order response dictionary
        """
        try:
            self.logger.info(
                f"Placing MARKET order: {side} {quantity} {symbol}"
            )
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            
            self.logger.info(
                f"Market order placed successfully. Order ID: {order.get('orderId')}"
            )
            self.logger.debug(f"Order response: {order}")
            
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            self.logger.error(f"Binance request error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing market order: {e}")
            raise
    
    def place_limit_order(
        self, 
        symbol: str, 
        side: str, 
        quantity: float, 
        price: float
    ) -> Dict[str, Any]:
        """Place a limit order.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY or SELL)
            quantity: Order quantity
            price: Order price
            
        Returns:
            Order response dictionary
        """
        try:
            self.logger.info(
                f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}"
            )
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",  # Good Till Cancel
                quantity=quantity,
                price=price
            )
            
            self.logger.info(
                f"Limit order placed successfully. Order ID: {order.get('orderId')}"
            )
            self.logger.debug(f"Order response: {order}")
            
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            self.logger.error(f"Binance request error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing limit order: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Get order status.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Order status dictionary
        """
        try:
            self.logger.debug(f"Fetching order status for {order_id}")
            order = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            self.logger.info(f"Order status: {order.get('status')}")
            return order
        except Exception as e:
            self.logger.error(f"Error getting order status: {e}")
            raise





