import yfinance as yf
from datetime import datetime, timedelta
import pytz
import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PORTFOLIO_FILE = "portfolio.json"
STARTING_CASH = 10000.0

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"cash": STARTING_CASH, "stocks": {}}

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=4)

def is_market_open():
    tz = pytz.timezone('US/Eastern')
    now = datetime.now(tz)
    if now.weekday() > 4:
        return False
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    return market_open <= now <= market_close

def get_stock_price(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        try:
            return float(ticker.fast_info['lastPrice'])
        except:
            hist = ticker.history(period="1d")
            if not hist.empty:
                return float(hist['Close'].iloc[-1])
            return None
    except:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/portfolio', methods=['GET'])
def api_portfolio():
    portfolio = load_portfolio()
    total_stock_value = 0.0
    stocks_data = []
    
    for ticker, shares in portfolio['stocks'].items():
        price = get_stock_price(ticker) or 0.0
        val = price * shares
        total_stock_value += val
        stocks_data.append({
            "ticker": ticker,
            "shares": shares,
            "current_price": price,
            "total_value": val
        })
        
    return jsonify({
        "cash": portfolio['cash'],
        "stocks": stocks_data,
        "total_portfolio_value": portfolio['cash'] + total_stock_value,
        "market_open": is_market_open()
    })

@app.route('/api/buy', methods=['POST'])
def api_buy():
    data = request.json
    ticker = data.get('ticker', '').upper().strip()
    shares = int(data.get('shares', 0))
    
    if not is_market_open():
        return jsonify({"success": False, "message": "Market is closed."})
    if shares <= 0:
        return jsonify({"success": False, "message": "Invalid share amount."})
        
    price = get_stock_price(ticker)
    if price is None:
        return jsonify({"success": False, "message": "Invalid ticker or price unavailable."})
        
    portfolio = load_portfolio()
    cost = price * shares
    if cost > portfolio['cash']:
        return jsonify({"success": False, "message": f"Insufficient funds. You need ${cost:,.2f}."})
        
    portfolio['cash'] -= cost
    portfolio['stocks'][ticker] = portfolio['stocks'].get(ticker, 0) + shares
    save_portfolio(portfolio)
    
    return jsonify({"success": True, "message": f"Successfully bought {shares} shares of {ticker}."})

@app.route('/api/sell', methods=['POST'])
def api_sell():
    data = request.json
    ticker = data.get('ticker', '').upper().strip()
    shares = int(data.get('shares', 0))
    
    if not is_market_open():
        return jsonify({"success": False, "message": "Market is closed."})
    if shares <= 0:
        return jsonify({"success": False, "message": "Invalid share amount."})
        
    portfolio = load_portfolio()
    owned = portfolio['stocks'].get(ticker, 0)
    
    if shares > owned:
        return jsonify({"success": False, "message": f"You only own {owned} shares of {ticker}."})
        
    price = get_stock_price(ticker)
    if price is None:
        return jsonify({"success": False, "message": "Price unavailable right now."})
        
    revenue = price * shares
    portfolio['cash'] += revenue
    portfolio['stocks'][ticker] -= shares
    
    if portfolio['stocks'][ticker] <= 0:
        del portfolio['stocks'][ticker]
        
    save_portfolio(portfolio)
    return jsonify({"success": True, "message": f"Successfully sold {shares} shares of {ticker}."})

@app.route('/api/timemachine', methods=['POST'])
def api_timemachine():
    data = request.json
    ticker = data.get('ticker', '').upper().strip()
    amount = float(data.get('amount', 0))
    years_ago = int(data.get('years', 1))
    
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*years_ago)
        
        hist = stock.history(start=start_date.strftime('%Y-%m-%d'), end=(start_date + timedelta(days=5)).strftime('%Y-%m-%d'))
        if hist.empty:
            return jsonify({"success": False, "message": "Could not fetch historical data."})
            
        old_price = float(hist['Close'].iloc[0])
        current_price = get_stock_price(ticker)
        
        if not current_price:
            return jsonify({"success": False, "message": "Could not fetch current price."})
            
        shares_bought = amount / old_price
        current_value = shares_bought * current_price
        profit = current_value - amount
        
        return jsonify({
            "success": True,
            "old_price": old_price,
            "current_price": current_price,
            "current_value": current_value,
            "profit": profit
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
