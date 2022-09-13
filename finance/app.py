# export API_KEY=pk_baa6d45acaa94e3d8e1bc638185c3794
# CREATE TABLE 'transactions'('di' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' INT, 'symbol' TEXT, 'shares' INT, 'price' REAL, 'date' timestamp);
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # index table
    rows = db.execute(
        "SELECT symbol, SUM(shares) FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    holdings = []
    all_total = 0

    for row in rows:
        stock = lookup(row['symbol'])
        sum_value = (stock["price"] * row["SUM(shares)"])
        holdings.append({"symbol": stock["symbol"], "name": stock["name"],
                         "shares": row["SUM(shares)"], "price": usd(stock["price"]), "total": usd(sum_value)})
        all_total += stock["price"] * row["SUM(shares)"]

    rows = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    cash = rows[0]["cash"]
    all_total += cash
    return render_template("index.html", holdings=holdings, cash=usd(cash), all_total=usd(all_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        shares = request.form.get("shares")
        symbol = request.form.get("symbol")
        stock = lookup(symbol.upper())

        # symbol needs to be submitted
        if not symbol:
            return apology("Provide the name of the share you want to buy.")

        elif stock == None:
            return apology("Share does not exist.")

        elif not shares.isdigit():
            return apology("Not a number.")

        # shares are less than 1
        elif int(shares) < 1:
            return apology("You must buy at least 1 share.")

        # transaction value
        transaction_val = int(shares) * stock['price']

        # check user cash for transaction
        usr_cash_db = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        cash = usr_cash_db[0]["cash"]

        # if user has less money than transaction value
        if cash < transaction_val:
            return apology("You don't have enough money.")

        # subtract user cash by the transaction value
        updt_cash = cash - transaction_val

        # update cash value for user
        db.execute("UPDATE users SET cash=? WHERE id=?", updt_cash, session["user_id"])

        # update transactions table
        date = datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], stock['symbol'], int(shares), stock["price"], date)
        flash("Bought")
        return redirect("/")

    # else for event via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions_db = db.execute(
        "SELECT symbol, shares, price, date, transacted FROM transactions WHERE user_id=?", session["user_id"])
    for i in range(len(transactions_db)):
        transactions_db[i]["price"] = usd(transactions_db[i]["price"])
    return render_template("history.html", transactions=transactions_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please insert user name.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please insert password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid user name and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if reached via POST
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Provide name of share.")

        # lookup
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        # check if stock is valid
        if stock == None:
            return apology("Share name not valid.")
        else:
            return render_template("quoted.html", stockSpec={'name': stock['symbol'], 'price': usd(stock['price'])})

    # if reached via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if reached via POST
    if request.method == "POST":

        # if username not submitted
        if not request.form.get("username"):
            return apology("Please insert user name.")

        # if password not submitted
        elif not request.form.get("password"):
            return apology("Please insert password.")

        # if password confirmation not submitted
        elif not request.form.get("confirmation"):
            return apology("Please confirm your password.")

        # if password confirmation is not the same as password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.")

        try:
            # register into database
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                                  request.form.get("username"), generate_password_hash(request.form.get("password")))
        except:
            # if username is taken
            return apology("User name is already taken.")

        # remember user session
        session["user_id"] = new_user

        # redirect to home page
        return redirect("/")

    # if user reached via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # reachev via POST
    if request.method == "POST":

        shares = request.form.get("shares")
        symbol = request.form.get("symbol")
        stock = lookup(symbol.upper())

        # if stock not submitted
        if not symbol:
            return apology("Provide the name of the share you want to sell.")

        elif stock == None:
            return apology("Share does not exist.")

        elif not shares.isdigit():
            return apology("Not a number.")

        elif int(shares) < 1:
            return apology("You must sell at least 1 share.")

        rows = db.execute(
            "SELECT symbol, SUM(shares) FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

        for row in rows:
            if row["symbol"] == symbol:
                if int(shares) > row["SUM(shares)"]:
                    return apology("sorry, something is wrong")

        transaction = int(shares) * stock['price']

        # check if user has enough cash
        usr_cash_db = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        cash = usr_cash_db[0]["cash"]

        # adds transaction value from user
        updt_cash = cash + transaction

        # update user cash
        db.execute("UPDATE users SET cash=? WHERE id=?", updt_cash, session["user_id"])

        # update transactions table
        date = datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], -1 * int(shares), stock["price"], date)
        flash("Sold")
        return redirect("/")

    # user reached via GET
    else:
        rows = db.execute(
            "SELECT symbol FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", symbols=[row["symbol"] for row in rows])


def errorhandler(e):
    """Error handler"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

