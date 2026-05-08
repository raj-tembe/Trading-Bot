"""
Binance Futures Client wrapper for testnet trading.
Handles authentication and API client initialization.
"""
import os
import logging
from binance.um_futures import UMFutures
from binance.error import ClientError

logger = logging.getLogger("trading_bot")


class BinanceFuturesClient:
    """
    Wrapper around Binance Futures API client configured for testnet.
    Handles initialization with testnet credentials from environment variables.
    """
    
    TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self):
        """
        Initialize Binance Futures client for testnet.
        
        Raises:
            ValueError: If API credentials are not found in environment
        """
        api_key = os.getenv("BINANCE_TESTNET_API_KEY")
        secret_key = os.getenv("BINANCE_TESTNET_SECRET_KEY")
        
        if not api_key or not secret_key:
            raise ValueError(
                "Missing API credentials. Please set BINANCE_TESTNET_API_KEY "
                "and BINANCE_TESTNET_SECRET_KEY environment variables."
            )
        
        try:
            self.client = UMFutures(
                key=api_key,
                secret=secret_key,
                base_url=self.TESTNET_BASE_URL
            )
            logger.info("Binance Futures testnet client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise
    
    def new_order(self, **kwargs):
        """
        Place a new futures order.
        
        Args:
            **kwargs: Order parameters (symbol, side, type, quantity, price, etc.)
        
        Returns:
            Order response dict
        
        Raises:
            ClientError: On Binance API errors
            Exception: On other unexpected errors
        """
        try:
            logger.debug(f"Placing order with parameters: {kwargs}")
            response = self.client.new_order(**kwargs)
            return response
        except ClientError as e:
            logger.error(f"Binance API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing order: {str(e)}")
            raise
