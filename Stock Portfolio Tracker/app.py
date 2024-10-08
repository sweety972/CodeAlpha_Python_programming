from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from stock_data import get_stock_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model to store stock information
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=True)

# Home route to show the portfolio
@app.route('/')
def index():
    # Query all stocks from the database
    stocks = Stock.query.all()

    # Make sure that `stocks` contains data
    for stock in stocks:
        stock_data = get_stock_data(stock.symbol)
        if stock_data and 'Time Series (Daily)' in stock_data:
            latest_day = list(stock_data['Time Series (Daily)'].keys())[0]
            stock.current_price = float(stock_data['Time Series (Daily)'][latest_day]['4. close'])
            db.session.commit()  # Update current prices in the database
        else:
            print(f"Failed to fetch data for {stock.symbol}: {stock_data}")  # Debugging print
    
    return render_template('index.html', stocks=stocks)

# Route to add stock to the portfolio
@app.route('/add_stock', methods=['POST'])
def add_stock():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    purchase_price = float(request.form['purchase_price'])
    new_stock = Stock(symbol=symbol, quantity=quantity, purchase_price=purchase_price)
    db.session.add(new_stock)
    db.session.commit()
    return redirect('/')

# Route to remove stock from the portfolio
@app.route('/remove_stock/<int:id>', methods=['POST'])
def remove_stock(id):
    stock = Stock.query.get(id)
    db.session.delete(stock)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables within the app context
    app.run(debug=True)
