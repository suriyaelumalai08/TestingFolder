from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

# ---------- MongoDB ----------
client = MongoClient("mongodb://localhost:27017/")
db = client["flask_app"]
users = db["users"]

# ---------- Flask ----------
app = Flask(__name__)
app.secret_key = "super_secret_key"

# ---------- Admin ----------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"


# ---------- HOME (Login / Register toggle) ----------
@app.route("/")
def home():
    page = request.args.get("page", "login")  # login or register
    return render_template("index.html", page=page)


# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # Admin login
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["role"] = "admin"
        return redirect("/admin")

    user = users.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        session["role"] = "user"
        return "User login successful"

    return "Invalid credentials"


# ---------- REGISTER ----------
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    age = int(request.form["age"])
    password = request.form["password"]

    if username == ADMIN_USERNAME:
        return "Username reserved"

    if users.find_one({"username": username}):
        return "User already exists"

    users.insert_one({
        "username": username,
        "age": age,
        "password": generate_password_hash(password)
    })

    return redirect("/?page=login")


# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access denied"

    user_list = users.find({}, {"_id": 0, "username": 1, "age": 1})
    return render_template("index.html", page="admin", users=user_list)


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
