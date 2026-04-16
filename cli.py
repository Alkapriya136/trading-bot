import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from bot.logging_config import setup_logging
from bot.orders import OrderManager

# Initialize rich console for better output
console = Console()


def print_order_summary(summary: dict):
    table = Table(title="Order Request Summary", show_header=True, header_style="bold magenta")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in summary.items():
        table.add_row(key.upper(), str(value))
    
    console.print(table)


def print_order_response(response: dict):
    table = Table(title="Order Response Details", show_header=True, header_style="bold blue")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="yellow")
    
    for key, value in response.items():
        table.add_row(key, str(value))
    
    console.print(table)


def cmd_place_order(args):
    logger = setup_logging()
    
    try:
        console.print("\n[bold cyan]🤖 Binance Futures Trading Bot[/bold cyan]\n")
        
        if args.testnet:
            console.print("[yellow] Using TESTNET mode[/yellow]\n")
        else:
            console.print("[red] WARNING: Using LIVE trading mode![/red]\n")
        
        # Initialize order manager
        logger.info(f"Initializing order manager (testnet={args.testnet})")
        order_manager = OrderManager(testnet=args.testnet)
        
        # Place order
        logger.info(f"Placing order: {args.symbol} {args.side} {args.order_type} {args.quantity} @ {args.price}")
        result = order_manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price
        )
        
        # Display results
        if result["success"]:
            console.print()
            print_order_summary(result["order_summary"])
            console.print()
            print_order_response(result["order_response"])
            console.print()
            
            success_msg = (
                f"Order placed successfully!\n"
                f"Order ID: {result['order_response']['orderId']}\n"
                f"Status: {result['order_response']['status']}"
            )
            console.print(Panel(success_msg, style="bold green", title="Success"))
            return 0
            
        else:
            error_msg = (
                f"❌ Order failed\n"
                f"Error Type: {result['error_type']}\n"
                f"Message: {result['error_message']}"
            )
            console.print(Panel(error_msg, style="bold red", title="Error"))
            return 1
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error in CLI: {e}")
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        return 1


def cmd_account(args):
    logger = setup_logging()
    
    try:
        console.print("\n[bold cyan]📊 Fetching Account Information...[/bold cyan]\n")
        
        from bot.client import BinanceFuturesClient
        client = BinanceFuturesClient(testnet=args.testnet)
        
        account_info = client.get_account_info()
        
        table = Table(title="Account Balance", show_header=True, header_style="bold magenta")
        table.add_column("Asset", style="cyan")
        table.add_column("Balance", style="green")
        table.add_column("Available", style="yellow")
        
        for asset in account_info.get("assets", [])[:10]:
            if float(asset.get("walletBalance", 0)) > 0:
                table.add_row(
                    asset.get("asset"),
                    asset.get("walletBalance"),
                    asset.get("availableBalance")
                )
        
        console.print(table)
        console.print(f"\n[green]Total Account Value (USDT): {account_info.get('totalWalletBalance', 'N/A')}[/green]\n")
        return 0
        
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        return 1


def cmd_symbol_info(args):
    logger = setup_logging()
    
    try:
        console.print(f"\n[bold cyan]🔍 Fetching Symbol Info for {args.symbol}...[/bold cyan]\n")
        
        from bot.client import BinanceFuturesClient
        client = BinanceFuturesClient(testnet=args.testnet)
        
        info = client.get_symbol_info(args.symbol.upper())
        
        if info:
            table = Table(title=f"Symbol: {args.symbol}", show_header=True, header_style="bold magenta")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            key_fields = ["symbol", "status", "baseAsset", "quoteAsset", "pricePrecision", "quantityPrecision"]
            for field in key_fields:
                if field in info:
                    table.add_row(field, str(info[field]))
            
            console.print(table)
            return 0
        else:
            console.print(f"[red]Symbol {args.symbol} not found[/red]")
            return 1
            
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Trading Bot - Place orders on testnet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market buy order
  %(prog)s place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  
  # Place a limit sell order
  %(prog)s place-order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
  
  # Get account information
  %(prog)s account
  
  # Get symbol information
  %(prog)s symbol-info BTCUSDT
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    place_parser = subparsers.add_parser('place-order', help='Place an order on Binance Futures')
    place_parser.add_argument('--symbol', required=True)
    place_parser.add_argument('--side', required=True, choices=['BUY', 'SELL', 'buy', 'sell'])
    place_parser.add_argument('--type', dest='order_type', required=True, choices=['MARKET', 'LIMIT', 'market', 'limit'])
    place_parser.add_argument('--quantity', type=float, required=True)
    place_parser.add_argument('--price', type=float)
    place_parser.add_argument('--testnet', action='store_true', default=True)
    place_parser.add_argument('--live', dest='testnet', action='store_false')
    place_parser.set_defaults(func=cmd_place_order)
    
    account_parser = subparsers.add_parser('account')
    account_parser.add_argument('--testnet', action='store_true', default=True)
    account_parser.add_argument('--live', dest='testnet', action='store_false')
    account_parser.set_defaults(func=cmd_account)
    
    symbol_parser = subparsers.add_parser('symbol-info')
    symbol_parser.add_argument('symbol')
    symbol_parser.add_argument('--testnet', action='store_true', default=True)
    symbol_parser.add_argument('--live', dest='testnet', action='store_false')
    symbol_parser.set_defaults(func=cmd_symbol_info)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())