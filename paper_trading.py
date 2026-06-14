import yfinance as yf
from datetime import datetime
import pytz
import json
import os

PORTFOLIO_FILE = "portfolio.json"
STARTING_CASH = 10000.0

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, 'r') as f:
                return json.load(f)
        except:
            print("Error loading portfolio file. Starting fresh.")
    
    return {"cash": STARTING_CASH, "stocks": {}}

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=4)

def is_market_open():
    """
    Checks if the US stock market is open.
    Mon-Fri, 9:30 AM to 4:00 PM Eastern Time.
    """
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz)
    
    # 0 = Monday, 4 = Friday
    if now.weekday() > 4:
        return False
        
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    return market_open <= now <= market_close

def get_stock_price(ticker_symbol):
    """
    Returns the current price of a stock using yfinance.
    If the ticker is invalid, returns None.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        # using fast_info or fallback to history
        try:
            return ticker.fast_info['lastPrice']
        except:
            hist = ticker.history(period="1d")
            if not hist.empty:
                return float(hist['Close'].iloc[-1])
            return None
    except Exception as e:
        return None

def display_portfolio(portfolio):
    print("\n" + "="*55)
    print("              MY PAPER TRADING PORTFOLIO")
    print("="*55)
    print(f"Available Cash: ${portfolio['cash']:,.2f}")
    
    stocks = portfolio['stocks']
    if not stocks:
        print("\nYou don't own any stocks yet.")
        print("="*55 + "\n")
        return
        
    print("\nOwned Stocks:")
    print(f"{'TICKER':<10} | {'SHARES':<10} | {'CURRENT PRICE':<15} | {'TOTAL VALUE'}")
    print("-" * 55)
    
    total_stock_value = 0.0
    
    for ticker, shares in stocks.items():
        price = get_stock_price(ticker)
        if price is None:
            print(f"{ticker:<10} | {shares:<10} | ERROR FETCHING  | ERROR")
            continue
            
        value = price * shares
        total_stock_value += value
        print(f"{ticker:<10} | {shares:<10} | ${price:>13,.2f} | ${value:,.2f}")
        
    total_portfolio_value = portfolio['cash'] + total_stock_value
    print("-" * 55)
    print(f"Total Stock Value: ${total_stock_value:,.2f}")
    print(f"TOTAL PORTFOLIO VALUE: ${total_portfolio_value:,.2f}")
    print("="*55 + "\n")

def buy_stock(portfolio):
    if not is_market_open():
        print("\n[!] The US Stock Market is currently CLOSED.")
        print("Market hours are Mon-Fri, 9:30 AM to 4:00 PM EST.")
        print("You cannot buy stocks right now.")
        return
        
    ticker = input("Enter the ticker symbol to buy (e.g., AAPL, TSLA): ").upper().strip()
    if not ticker:
        return
        
    print(f"Fetching current price for {ticker}...")
    price = get_stock_price(ticker)
    
    if price is None:
        print(f"[!] Could not find price for '{ticker}'. Are you sure it's correct?")
        return
        
    print(f"\nCurrent price of {ticker}: ${price:,.2f}")
    print(f"Your available cash: ${portfolio['cash']:,.2f}")
    
    try:
        shares_to_buy = int(input(f"How many shares of {ticker} do you want to buy? (0 to cancel): "))
    except ValueError:
        print("[!] Please enter a valid whole number.")
        return
        
    if shares_to_buy <= 0:
        print("Purchase cancelled.")
        return
        
    total_cost = shares_to_buy * price
    
    if total_cost > portfolio['cash']:
        print(f"[!] Insufficient funds! You need ${total_cost:,.2f} but only have ${portfolio['cash']:,.2f}.")
        return
        
    # Execute purchase
    portfolio['cash'] -= total_cost
    
    if ticker in portfolio['stocks']:
        portfolio['stocks'][ticker] += shares_to_buy
    else:
        portfolio['stocks'][ticker] = shares_to_buy
        
    save_portfolio(portfolio)
    print(f"\n[+] SUCCESS! You bought {shares_to_buy} shares of {ticker} for ${total_cost:,.2f}.")

def sell_stock(portfolio):
    if not is_market_open():
        print("\n[!] The US Stock Market is currently CLOSED.")
        print("Market hours are Mon-Fri, 9:30 AM to 4:00 PM EST.")
        print("You cannot sell stocks right now.")
        return
        
    if not portfolio['stocks']:
        print("\n[!] You don't have any stocks to sell.")
        return
        
    ticker = input("Enter the ticker symbol to sell (e.g., AAPL): ").upper().strip()
    
    if ticker not in portfolio['stocks'] or portfolio['stocks'][ticker] <= 0:
        print(f"[!] You don't own any shares of {ticker}.")
        return
        
    owned_shares = portfolio['stocks'][ticker]
    
    print(f"Fetching current price for {ticker}...")
    price = get_stock_price(ticker)
    
    if price is None:
        print(f"[!] Could not fetch the current price for {ticker}. Try again later.")
        return
        
    print(f"\nYou currently own {owned_shares} shares of {ticker}.")
    print(f"Current price of {ticker}: ${price:,.2f}")
    
    try:
        shares_to_sell = int(input(f"How many shares do you want to sell? (1-{owned_shares}, 0 to cancel): "))
    except ValueError:
        print("[!] Please enter a valid whole number.")
        return
        
    if shares_to_sell <= 0:
        print("Sale cancelled.")
        return
        
    if shares_to_sell > owned_shares:
        print(f"[!] You can't sell more than you own ({owned_shares} shares).")
        return
        
    # Execute sale
    total_revenue = shares_to_sell * price
    portfolio['cash'] += total_revenue
    portfolio['stocks'][ticker] -= shares_to_sell
    
    # Remove from dictionary if 0 shares left
    if portfolio['stocks'][ticker] == 0:
        del portfolio['stocks'][ticker]
        
    save_portfolio(portfolio)
    print(f"\n[+] SUCCESS! You sold {shares_to_sell} shares of {ticker} for ${total_revenue:,.2f}.")

def print_menu():
    print("\n--- MAIN MENU ---")
    print("1. View Portfolio")
    print("2. Check a Stock Price")
    print("3. Buy Stock")
    print("4. Sell Stock")
    print("5. Market Status (Open/Closed?)")
    print("6. Exit")

def main():
    print("="*50)
    print("  WELCOME TO THE PAPER TRADING SIMULATOR  ")
    print("="*50)
    
    portfolio = load_portfolio()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            display_portfolio(portfolio)
        elif choice == '2':
            ticker = input("Enter ticker symbol (e.g., MSFT): ").upper().strip()
            if ticker:
                print(f"Fetching price for {ticker}...")
                price = get_stock_price(ticker)
                if price is not None:
                    print(f"The current price of {ticker} is ${price:,.2f}")
                else:
                    print(f"[!] Could not fetch price for '{ticker}'.")
        elif choice == '3':
            buy_stock(portfolio)
        elif choice == '4':
            sell_stock(portfolio)
        elif choice == '5':
            if is_market_open():
                print("\n[+] The US Stock Market is currently OPEN.")
            else:
                print("\n[-] The US Stock Market is currently CLOSED.")
        elif choice == '6':
            print("\nSaving portfolio... Goodbye! Happy trading!")
            save_portfolio(portfolio)
            break
        else:
            print("\n[!] Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
