import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Trading configuration
SLIPPAGE = float(os.getenv('SLIPPAGE', '0.001'))  # Default slippage: 0.1%

# Symbol to product ID mapping
SYMBOL_TO_PRODUCT_ID = {
    # Standard format
    'ETHUSD': 1,
    'BTCUSD': 2,
    'BNBUSD': 3,
    # USDT format
    'ETHUSDT': 1,
    'BTCUSDT': 2,
    'BNBUSDT': 3
}