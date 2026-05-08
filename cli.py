"""
Command-line interface for the trading bot.
Handles user input, validation, and order placement.
"""
import sys
import argparse
import logging

from bot.logging_config import setup_logging
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.client import BinanceFuturesClient
from bot.orders import place_order


def setup_argparse() -> argparse.ArgumentParser:
    """
    Set up command-line argument parser.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Market order: python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.1
  Limit order:  python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.1 --price 45000
        """
    )
    
    parser.add_argument(
        "--symbol",
        required=True,
        type=str,
        help="Trading symbol (e.g., BTCUSDT)"
    )
    
    parser.add_argument(
        "--side",
        required=True,
        type=str,
        choices=["BUY", "SELL"],
        help="Order side"
    )
    
    parser.add_argument(
        "--order_type",
        required=True,
        type=str,
        choices=["MARKET", "LIMIT"],
        help="Order type"
    )
    
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity in contracts (must be > 0)"
    )
    
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Order price (required for LIMIT orders, not for MARKET)"
    )
    
    return parser


def validate_and_prepare_order(args) -> dict:
    """
    Validate all order parameters.
    
    Args:
        args: Parsed command-line arguments
    
    Returns:
        Dictionary with validated parameters
    
    Raises:
        ValueError: On validation failure
    """
    symbol = validate_symbol(args.symbol)
    side = validate_side(args.side)
    order_type = validate_order_type(args.order_type)
    quantity = validate_quantity(args.quantity)
    
    # Validate price based on order type
    price = validate_price(args.price, order_type)
    
    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
    }


def print_order_summary(order_params: dict) -> None:
    """
    Print a clear summary before sending the order.
    
    Args:
        order_params: Dictionary with order parameters
    """
    print("\n" + "=" * 60)
    print("ORDER SUMMARY")
    print("=" * 60)
    print(f"Symbol:      {order_params['symbol']}")
    print(f"Side:        {order_params['side']}")
    print(f"Type:        {order_params['order_type']}")
    print(f"Quantity:    {order_params['quantity']}")
    if order_params['price']:
        print(f"Price:       {order_params['price']}")
    print("=" * 60)
    print("Sending order...\n")


def print_order_response(response: dict) -> None:
    """
    Print order response details.
    
    Args:
        response: Order response dictionary from Binance API
    """
    print("\n" + "=" * 60)
    print("ORDER RESPONSE")
    print("=" * 60)
    print(f"Order ID:        {response.get('orderId')}")
    print(f"Status:          {response.get('status')}")
    print(f"Executed Qty:    {response.get('executedQty')}")
    print(f"Avg Price:       {response.get('avgPrice', 'N/A')}")
    print(f"Symbol:          {response.get('symbol')}")
    print(f"Side:            {response.get('side')}")
    print(f"Type:            {response.get('type')}")
    print("=" * 60)
    print("✓ Order placed successfully!\n")


def print_error_message(error: Exception) -> None:
    """
    Print a clean error message.
    
    Args:
        error: Exception that occurred
    """
    print("\n" + "=" * 60)
    print("ERROR")
    print("=" * 60)
    print(f"✗ {str(error)}")
    print("=" * 60 + "\n")


def main() -> int:
    """
    Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Setup logging
    logger = setup_logging()
    logger.info("Trading bot started")
    
    # Parse arguments
    parser = setup_argparse()
    args = parser.parse_args()
    
    try:
        # Validate and prepare order
        logger.info(f"Validating order parameters...")
        order_params = validate_and_prepare_order(args)
        
        # Print pre-order summary
        print_order_summary(order_params)
        
        # Initialize Binance client
        logger.info("Initializing Binance Futures client...")
        client = BinanceFuturesClient()
        
        # Place order
        response = place_order(
            client=client,
            symbol=order_params["symbol"],
            side=order_params["side"],
            order_type=order_params["order_type"],
            quantity=order_params["quantity"],
            price=order_params["price"],
        )
        
        # Print response
        print_order_response(response)
        logger.info("Order placement completed successfully")
        
        return 0
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        print_error_message(e)
        return 1
    
    except ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        print_error_message(e)
        return 1
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print_error_message(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
