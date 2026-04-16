"# Binance Futures Trading Bot 🤖

A Python CLI application for placing orders on Binance Futures Testnet (USDT-M). This bot provides a clean, reusable structure with proper logging and error handling.

## 📋 Features

- ✅ **Order Types**: Market and Limit orders
- ✅ **Order Sides**: BUY and SELL
- ✅ **CLI Interface**: User-friendly command-line interface with Typer
- ✅ **Input Validation**: Comprehensive validation for all parameters
- ✅ **Logging**: Structured logging to both file and console
- ✅ **Error Handling**: Robust error handling for API errors, network failures, and invalid inputs
- ✅ **Clean Architecture**: Separated client/API layer and CLI layer
- ✅ **Rich Output**: Formatted tables and colored output for better readability

## 🏗️ Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance Futures API client wrapper
│   ├── orders.py         # Order placement logic
│   ├── validators.py     # Input validation
│   └── logging_config.py # Logging configuration
├── cli.py                # CLI entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## 🚀 Setup

### Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account (register at https://testnet.binancefuture.com)
- API Key and Secret Key from Binance Futures Testnet

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd /app/trading_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API credentials**
   
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Binance Futures Testnet credentials:
   ```env
   BINANCE_API_KEY=your_api_key_here
   BINANCE_SECRET_KEY=your_secret_key_here
   BINANCE_TESTNET_URL=https://testnet.binancefuture.com
   ```

### Getting API Credentials

1. Go to https://testnet.binancefuture.com
2. Login or register for a testnet account
3. Navigate to API Management
4. Generate API Key and Secret Key
5. Copy them to your `.env` file

## 📖 Usage

### Basic Commands

The CLI provides several commands for interacting with Binance Futures:

#### 1. Place Market Order

```bash
python cli.py place-order \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

**Short version:**
```bash
python cli.py place-order -s BTCUSDT -d BUY -t MARKET -q 0.001
```

#### 2. Place Limit Order

```bash
python cli.py place-order \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.001 \
  --price 45000
```

**Short version:**
```bash
python cli.py place-order -s BTCUSDT -d SELL -t LIMIT -q 0.001 -p 45000
```

#### 3. Get Account Information

```bash
python cli.py account
```

#### 4. Get Symbol Information

```bash
python cli.py symbol-info BTCUSDT
```

### Command Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--symbol` | `-s` | Trading pair symbol (e.g., BTCUSDT) | Yes |
| `--side` | `-d` | Order side: BUY or SELL | Yes |
| `--type` | `-t` | Order type: MARKET or LIMIT | Yes |
| `--quantity` | `-q` | Order quantity | Yes |
| `--price` | `-p` | Order price (required for LIMIT) | For LIMIT only |
| `--testnet/--live` | | Use testnet (default) or live trading | No (default: testnet) |

### Help

Get help for any command:
```bash
python cli.py --help
python cli.py place-order --help
```

## 📊 Example Output

### Market Order Success

```
🤖 Binance Futures Trading Bot

⚠️  Using TESTNET mode

┏━━━━━━━━━━━━━━━━━━━━━━━━━ Order Request Summary ━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Parameter  ┃ Value                                                          ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ SYMBOL     │ BTCUSDT                                                        │
│ SIDE       │ BUY                                                            │
│ TYPE       │ MARKET                                                         │
│ QUANTITY   │ 0.001                                                          │
│ PRICE      │ MARKET                                                         │
└────────────┴────────────────────────────────────────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━ Order Response Details ━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Field        ┃ Value                                                        ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ orderId      │ 12345678                                                     │
│ status       │ FILLED                                                       │
│ executedQty  │ 0.001                                                        │
│ avgPrice     │ 43250.50                                                     │
└──────────────┴──────────────────────────────────────────────────────────────┘

╭──────────────────────────────── Success ─────────────────────────────────╮
│ ✅ Order placed successfully!                                            │
│ Order ID: 12345678                                                       │
│ Status: FILLED                                                           │
╰──────────────────────────────────────────────────────────────────────────╯
```

## 📝 Logging

All operations are logged to files in `/app/logs/` directory with timestamps:
- File: `/app/logs/trading_bot_YYYYMMDD_HHMMSS.log`
- Format: `YYYY-MM-DD HH:MM:SS - logger_name - LEVEL - message`

Example log entries:
```
2025-08-20 10:30:45 - trading_bot - INFO - Logging initialized. Log file: /app/logs/trading_bot_20250820_103045.log
2025-08-20 10:30:46 - trading_bot.client - INFO - Connected to Binance Futures TESTNET
2025-08-20 10:30:47 - trading_bot.orders - INFO - Validating order parameters
2025-08-20 10:30:48 - trading_bot.client - INFO - Market order placed successfully. Order ID: 12345678
```

## 🛡️ Error Handling

The bot handles various error scenarios:

1. **Validation Errors**: Invalid symbol, side, order type, quantity, or price
2. **API Errors**: Binance API errors with status codes
3. **Network Errors**: Connection failures and timeouts
4. **Authentication Errors**: Invalid API credentials

Example error output:
```
╭──────────────────────────────── Error ───────────────────────────────────╮
│ ❌ Order failed                                                          │
│ Error Type: ValidationError                                              │
│ Message: Quantity must be positive: -0.001                               │
╰──────────────────────────────────────────────────────────────────────────╯
```

## 🧪 Testing

### Manual Testing

1. **Test Market Order** (BUY):
   ```bash
   python cli.py place-order -s BTCUSDT -d BUY -t MARKET -q 0.001
   ```

2. **Test Limit Order** (SELL):
   ```bash
   python cli.py place-order -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3000
   ```

3. **Check Account Balance**:
   ```bash
   python cli.py account
   ```

4. **Verify Symbol**:
   ```bash
   python cli.py symbol-info BTCUSDT
   ```

### Reviewing Logs

After testing, check the log files in `/app/logs/` directory:
```bash
ls -la /app/logs/
tail -f /app/logs/trading_bot_*.log
```

## 📦 Dependencies

- `python-binance==1.0.19` - Official Binance Python library
- `typer==0.12.3` - Modern CLI framework
- `rich==13.7.1` - Rich text and formatting
- `python-dotenv==1.0.1` - Environment variable management
- `requests==2.31.0` - HTTP library
- `pydantic==2.6.4` - Data validation

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BINANCE_API_KEY` | Your Binance API key | `abc123...` |
| `BINANCE_SECRET_KEY` | Your Binance secret key | `xyz789...` |
| `BINANCE_TESTNET_URL` | Binance testnet URL | `https://testnet.binancefuture.com` |

### Order Parameters

- **Symbol**: Must end with USDT (e.g., BTCUSDT, ETHUSDT)
- **Side**: BUY or SELL
- **Type**: MARKET or LIMIT
- **Quantity**: Must be positive (e.g., 0.001)
- **Price**: Required for LIMIT orders, must be positive

## 🔒 Security

- API credentials are stored in `.env` file (not committed to version control)
- API keys are masked in logs (shows first 8 and last 4 characters only)
- Default mode is TESTNET to prevent accidental live trading
- Use `--live` flag with caution for production trading

## 📄 Assumptions

1. Using Binance Futures Testnet for development and testing
2. Trading USDT-M perpetual futures contracts
3. All symbols should end with USDT
4. Quantities and prices must be positive numbers
5. Limit orders use GTC (Good Till Cancel) time in force
6. Testnet mode is default for safety

## 🚧 Future Enhancements (Optional)

- [ ] Add more order types (Stop-Limit, OCO, TWAP)
- [ ] Interactive CLI with menus and prompts
- [ ] Order history and status tracking
- [ ] Position management
- [ ] Risk management features
- [ ] Web-based UI
- [ ] Real-time price monitoring

## 📞 Support

For issues or questions:
1. Check the logs in `/app/logs/`
2. Verify API credentials in `.env`
3. Ensure you're using Binance Futures Testnet
4. Check Binance API documentation: https://binance-docs.github.io/apidocs/futures/en/

## 📜 License

This project is created for educational and testing purposes.

---

**⚠️ Disclaimer**: This bot is for educational purposes only. Always test on testnet before using with real funds. Trading cryptocurrencies carries risk.
"
Observation: Create successful: /app/trading_bot/README.md