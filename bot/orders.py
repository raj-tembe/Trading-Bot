"""
Order placement logic for the trading bot.
Handles order creation, logging, and error handling.
"""
import logging
import requests
from binance.error import ClientError

logger = logging.getLogger("trading_bot")


def place_order(client, symbol: str, side: str, order_type: str, 
                quantity: float, price: float = None) -> dict:
    """
    Place an order on Binance Futures testnet.
    
    Args:
        client: BinanceFuturesClient instance
        symbol: Trading symbol (e.g., BTCUSDT)
        side: Order side (BUY or SELL)
        order_type: Order type (MARKET or LIMIT)
        quantity: Order quantity in contracts
        price: Order price (required for LIMIT, None for MARKET)
    
    Returns:
        Order response dictionary
    
    Raises:
        ValueError: On API errors (wraps ClientError)
        ConnectionError: On network errors
        Exception: On unexpected errors
    """
    try:
        # Build order parameters
        order_params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        
        # Add price for LIMIT orders
        if order_type == "LIMIT" and price is not None:
            order_params["price"] = price
        
        # Log order request (without sensitive keys)
        logger.info(
            f"Placing {order_type} {side} order: {symbol} qty={quantity} "
            f"{f'price={price}' if price else ''}"
        )
        logger.debug(f"Order parameters: {order_params}")
        
        # Place the order
        response = client.new_order(**order_params)
        
        # Log successful order
        logger.info(
            f"Order placed successfully. OrderID: {response.get('orderId')}, "
            f"Status: {response.get('status')}, "
            f"ExecutedQty: {response.get('executedQty')}, "
            f"AvgPrice: {response.get('avgPrice', 'N/A')}"
        )
        logger.debug(f"Full order response: {response}")
        
        return response
    
    except ClientError as e:
        error_msg = f"Binance API Error: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: Unable to connect to Binance. {str(e)}"
        logger.error(error_msg)
        raise ConnectionError(error_msg)
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        raise
