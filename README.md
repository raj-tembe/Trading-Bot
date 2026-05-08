# Binance Futures Trading Bot (Testnet)

A production-ready CLI trading bot for Binance Futures Testnet (USDT-M) built with Python. Supports placing market and limit orders with full validation, error handling, and structured logging.

## Features

- ✅ Market and Limit order support
- ✅ BUY and SELL order sides
- ✅ Strict input validation
- ✅ Comprehensive logging to file and console
- ✅ Error handling for API and network failures
- ✅ Clear CLI interface with argparse
- ✅ Environment-based API credential management
- ✅ Testnet-only configuration

## Setup

### 1. Clone and Create Virtual Environment

```bash
cd /path/to/Trading-Bot
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Export your Binance Testnet API credentials:

```bash
export BINANCE_TESTNET_API_KEY="your_testnet_api_key_here"
export BINANCE_TESTNET_SECRET_KEY="your_testnet_secret_key_here"
```

**Permanently** (add to `.bashrc`, `.zshrc`, or `.env` file for your IDE):

```bash
# Add to ~/.bashrc or ~/.zshrc
export BINANCE_TESTNET_API_KEY="your_testnet_api_key_here"
export BINANCE_TESTNET_SECRET_KEY="your_testnet_secret_key_here"
```

Or create a `.env` file in the project root (not committed to version control):

```
BINANCE_TESTNET_API_KEY=your_testnet_api_key_here
BINANCE_TESTNET_SECRET_KEY=your_testnet_secret_key_here
```

Then load it before running:

```bash
source .env
python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.1
```

### 4. Obtain Testnet API Keys

1. Go to [Binance Testnet Futures](https://testnet.binancefuture.com/)
2. Create an account or log in
3. Navigate to **API Management** (or **Developer** menu)
4. Create a new API key
5. Copy the **API Key** and **Secret Key**
6. Set them as environment variables (see step 3)

## Usage

### Market Order Example

Place a market BUY order for 0.1 BTC:

```bash
python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.1
```

Place a market SELL order for 0.1 ETH:

```bash
python cli.py --symbol ETHUSDT --side SELL --order_type MARKET --quantity 0.1
```

### Limit Order Example

Place a limit BUY order at a specific price:

```bash
python cli.py --symbol BTCUSDT --side BUY --order_type LIMIT --quantity 0.1 --price 45000
```

Place a limit SELL order:

```bash
python cli.py --symbol ETHUSDT --side SELL --order_type LIMIT --quantity 0.1 --price 3000
```

### Command-Line Arguments

- `--symbol` (required): Trading symbol (e.g., `BTCUSDT`, `ETHUSDT`)
- `--side` (required): Order side (`BUY` or `SELL`)
- `--order_type` (required): Order type (`MARKET` or `LIMIT`)
- `--quantity` (required): Order quantity in contracts (must be > 0)
- `--price` (optional): Order price (required only for LIMIT orders)

### Help

```bash
python cli.py --help
```

## Output Example

### Successful Market Order

```
============================================================
ORDER SUMMARY
============================================================
Symbol:      BTCUSDT
Side:        BUY
Type:        MARKET
Quantity:    0.1
============================================================
Sending order...

============================================================
ORDER RESPONSE
============================================================
Order ID:        12345678
Status:          FILLED
Executed Qty:    0.1
Avg Price:       45678.50
Symbol:          BTCUSDT
Side:            BUY
Type:            MARKET
============================================================
✓ Order placed successfully!
```

### Error Example

```
============================================================
ERROR
============================================================
✗ Validation error: Quantity must be greater than 0. Received: -0.5
============================================================
```

## Logging

All API requests, responses, and errors are logged to `trading_bot.log` in the project root.

### Log File Format

```
2026-05-08 14:23:45 - trading_bot - INFO - Binance Futures testnet client initialized successfully
2026-05-08 14:23:45 - trading_bot - INFO - Placing MARKET BUY order: BTCUSDT qty=0.1 
2026-05-08 14:23:46 - trading_bot - INFO - Order placed successfully. OrderID: 12345678, Status: FILLED, ExecutedQty: 0.1, AvgPrice: 45678.50
```

Console output shows INFO level and above, while the file logs DEBUG level and above for detailed troubleshooting.

## Project Structure

```
trading_bot/
  bot/
    __init__.py                 # Package initializer
    client.py                   # Binance Futures client wrapper
    orders.py                   # Order placement logic
    validators.py               # Input validation functions
    logging_config.py           # Logging setup
  cli.py                        # Command-line interface entry point
  README.md                     # This file
  requirements.txt              # Python dependencies
  trading_bot.log               # Generated at runtime
```

## Key Implementation Details

### Validators (`bot/validators.py`)

- `validate_symbol(symbol)`: Checks symbol format (alphanumeric, 3-20 chars)
- `validate_side(side)`: Ensures side is BUY or SELL
- `validate_order_type(order_type)`: Ensures type is MARKET or LIMIT
- `validate_quantity(quantity)`: Ensures quantity > 0
- `validate_price(price, order_type)`: Validates price for LIMIT orders only

### Client (`bot/client.py`)

- `BinanceFuturesClient`: Initializes Binance Futures client with testnet URL
- Reads API credentials from `BINANCE_TESTNET_API_KEY` and `BINANCE_TESTNET_SECRET_KEY` environment variables
- No hardcoded credentials

### Orders (`bot/orders.py`)

- `place_order()`: Places orders with logging and error handling
- Catches `BinanceAPIException` and re-raises as `ValueError`
- Catches network errors and re-raises as `ConnectionError`
- Logs request payloads and full responses

### CLI (`cli.py`)

- Uses `argparse` for clean command-line interface
- Validates inputs before sending to Binance
- Prints clear order summary before execution
- Prints order response on success
- Returns appropriate exit codes (0 success, 1 failure)

## Assumptions

- **Quantity Unit**: Quantity is specified in contract numbers (e.g., 0.1 BTC, 1 ETH), not in USDT
- **Leverage**: Default 1x leverage (no position size multiplier)
- **Testnet Only**: This bot is configured for testnet only. To use mainnet, change the base URL and environment variable names
- **No Position Management**: This bot only places new orders; it does not manage existing positions or close trades
- **Decimal Precision**: Binance will validate quantity and price precision based on symbol requirements

## Error Handling

The bot gracefully handles:

- **Invalid User Input**: Validation errors with descriptive messages
- **API Errors**: BinanceAPIException caught and re-raised with user-friendly text
- **Network Failures**: Connection errors handled separately with helpful messages
- **Unexpected Errors**: Caught and logged without crashing

All errors are logged to both file and console.

## Dependencies

- `python-binance==1.0.19`: Official Binance Python SDK
- `requests>=2.28.0`: HTTP library (dependency of python-binance)

See `requirements.txt` for the complete list.

## Troubleshooting

### "Missing API credentials" Error

Ensure environment variables are set:

```bash
echo $BINANCE_TESTNET_API_KEY
echo $BINANCE_TESTNET_SECRET_KEY
```

### "Connection refused" Error

Verify the testnet URL is accessible:

```bash
curl https://testnet.binancefuture.com/fapi/v1/time
```

### "Invalid symbol" Error

Ensure the symbol exists on Binance Futures testnet. Common symbols: `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `XRPUSDT`

### Logs Not Appearing

Check that `trading_bot.log` exists in the project root. Logs are written in real-time.

## License

See LICENSE file.

## Support

For issues with the trading bot, check the logs in `trading_bot.log` for detailed error messages.

---

**⚠️ IMPORTANT**: This bot is for **testnet only**. Do not use with mainnet credentials without thorough testing and understanding of the risks.