import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///games.db")


@app.route("/")
def index():
    """Show button to start playing"""

    return render_template("index.html")

@app.route("/jugar", methods=["GET", "POST"])
@login_required
def jugar():
    if request.method == "POST" and request.form["apuesta"] == "Apostar":
        session["cantidad_apostada"] = request.form.get("cantidad_apostada")

        if float(session["cantidad_apostada"]) == False:
            return apology("Tenes que apostar un número mayor a 0", 403)

        if not session["cantidad_apostada"] or float(session["cantidad_apostada"]) <= 0:
            return apology("Tenes que apostar un número mayor a 0", 403)

        get_user_data = db.execute("SELECT username, money FROM users WHERE id = :user_id", user_id=session["user_id"])

        username = get_user_data[0]["username"]
        current_money = get_user_data[0]["money"]
        updated_current_money = current_money - float(session["cantidad_apostada"])
        if updated_current_money < 0:
            session["cantidad_apostada"] = 0
            return apology("No tenés esa cantidad de dinero disponible para apostar", 403)

        db.execute("UPDATE users SET money = :updated_current_money WHERE id = :user_id", updated_current_money=updated_current_money, user_id=session["user_id"])

        return redirect("/apostando")


    if request.method == "GET":
        try:
            get_user_data = db.execute("SELECT username, money FROM users WHERE id = :user_id", user_id=session["user_id"])

            username = get_user_data[0]["username"]
            money = round(get_user_data[0]["money"], 2)

            last_10_transactions_dict = db.execute("SELECT * FROM history WHERE username = :username ORDER BY id DESC LIMIT 10", username=username)

        except:
            return redirect("/entrar")

        return render_template("jugar.html", username=username, money=money, last_10_transactions_dict=last_10_transactions_dict)

@app.route("/apostando", methods=["GET", "POST"])
@login_required
def apostando():

    if request.method == "POST":

        #String result of user cash out
        user_result = request.form.get("uptrend_multiplier")

        cantidad_apostada = float(session.get('cantidad_apostada', None))
        cantidad_apostada_str = session.get('cantidad_apostada', None)

        #NEXT GAME NUMBER
        next_game_dict = db.execute("SELECT nextgame FROM nextgame WHERE id = :id", id = 1)
        next_game = next_game_dict[0]["nextgame"]

        #BUST NUMBER
        current_multiplier_dict = db.execute("SELECT multiplier FROM games WHERE id=:next_game", next_game=next_game)
        current_multiplier = current_multiplier_dict[0]["multiplier"]

        #GET USERNAME
        get_user_data = db.execute("SELECT username, money FROM users WHERE id = :user_id", user_id=session["user_id"])
        username = get_user_data[0]["username"]

        #GET HASH
        get_hash_dict = db.execute("SELECT hash FROM games WHERE id=:next_game", next_game=next_game)
        game_hash = get_hash_dict[0]["hash"]


        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")

        if user_result == "JUEGO TERMINADO!":
            user_result = "lost"
            rounded_result = 0.00
            cashed_out = "NO"
            earnings = 0.00

        else:
            user_result = float(request.form.get("uptrend_multiplier"))
            rounded_result = round(user_result, 2)
            cashed_out = request.form.get("uptrend_multiplier")

            winning_amount = round(cantidad_apostada * rounded_result, 2)
            earnings = round(winning_amount - cantidad_apostada, 2)

            db.execute("UPDATE users SET money = money + :winning_amount WHERE id = :user_id", winning_amount=winning_amount, user_id=session["user_id"])


        db.execute("INSERT INTO history (username, hash, bust, cashed_out, bet, earnings, date) VALUES(:username, :game_hash, :bust, :cashed_out, :bet, :earnings, :date)",
        username=username, game_hash=game_hash, bust=current_multiplier, cashed_out=cashed_out, bet=cantidad_apostada_str, earnings=earnings, date=date)


        return redirect("/jugar")


    if request.method == "GET":
        try:
            get_user_data = db.execute("SELECT username, money FROM users WHERE id = :user_id", user_id=session["user_id"])

            username = get_user_data[0]["username"]
            money = round(get_user_data[0]["money"],2)
        except:
            return redirect("/jugar")

        # 10.000 GAMES CREATED

        db.execute("UPDATE nextgame SET nextgame = nextgame - 1 WHERE id = 1")
        next_game_dict = db.execute("SELECT nextgame FROM nextgame WHERE id = :id", id = 1)
        next_game = next_game_dict[0]["nextgame"]

        cantidad_apostada = session.get('cantidad_apostada', None)



        current_multiplier_dict = db.execute("SELECT multiplier FROM games WHERE id=:next_game", next_game=next_game)

        current_multiplier = current_multiplier_dict[0]["multiplier"]

        data = {'game_multiplier': current_multiplier}

        last_transactions_dict = db.execute("SELECT * FROM history ORDER BY id DESC LIMIT 20")



        return render_template("apostando.html", username=username, money=money, cantidad_apostada=cantidad_apostada, data=data, last_transactions_dict=last_transactions_dict)


@app.route("/mihistorial")
@login_required
def history():
    """Show history of transactions"""

    get_user_data = db.execute("SELECT username, money FROM users WHERE id = :user_id", user_id=session["user_id"])

    username = get_user_data[0]["username"]
    money = round(get_user_data[0]["money"], 2)

    last_transactions_dict = db.execute("SELECT * FROM history WHERE username = :username ORDER BY id DESC", username=username)

    return render_template("mihistorial.html", username=username, money=money, last_transactions_dict=last_transactions_dict)




@app.route("/entrar", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to play the game
        return redirect("/jugar")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("entrar.html")


@app.route("/salir")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/registrarse", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if not request.form.get("username") or len(rows) == 1:
            return apology("You can not leave this empty or username is already in use", 403)
        else:
            correct_username = request.form.get("username")

        if request.form.get("password") != request.form.get("confirmation") or len(request.form.get("password")) == 0:
            return apology("Passwords does not match or are empty", 403)
        else:
            correct_password = request.form.get("password")
            hashed_password = generate_password_hash(correct_password)

        start_money = 10000.00

        new_user = db.execute("INSERT INTO users (username, password, money) VALUES(:correct_username, :hashed_password, :start_money)",
        correct_username=correct_username, hashed_password=hashed_password, start_money=start_money)

        session["user_id"] = new_user

        return redirect("/jugar")

    if request.method == "GET":
        return render_template("registrarse.html")

@app.route("/questions")
def questions():
    try:
        get_user_data = db.execute("SELECT username, money FROM users WHERE id = :user_id", user_id=session["user_id"])

        username = get_user_data[0]["username"]
        money = round(get_user_data[0]["money"], 2)

    except:
        return redirect("/entrar")

    return render_template("preguntas.html", username=username, money=money)


@app.route("/ranking")
@login_required
def ranking():
    try:
        get_user_data = db.execute("SELECT username, money FROM users WHERE id = :user_id", user_id=session["user_id"])

        username = get_user_data[0]["username"]
        money = round(get_user_data[0]["money"], 2)

    except:
        return redirect("/entrar")

    get_ranking_data = db.execute("SELECT username, money FROM users ORDER BY money DESC LIMIT 5")
    dict_len = len(get_ranking_data)
    for i in range(0, dict_len):
        get_ranking_data[i]["money"] = round(get_ranking_data[i]["money"]) - 10000
        get_ranking_data[i]["position"] = i + 1

    return render_template("ranking.html", username=username, money=money, get_ranking_data=get_ranking_data)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
