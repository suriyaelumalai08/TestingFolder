from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

# ------------------ MongoDB ------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["flask_app"]
users = db["users"]

# ------------------ Flask App ------------------
app = Flask(__name__)
# app.secret_key = "super_secret_key_123"   

# ------------------ Admin Credentials ------------------
ADMIN_USERNAME = "suriya@123"
ADMIN_PASSWORD = "123"


# ------------------ LOGIN ------------------
@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        user_name = request.form["username"]
        user_password = request.form["password"]

        # ✅ Admin login (NO DB)
        if user_name == ADMIN_USERNAME and user_password == ADMIN_PASSWORD:
            return redirect("/admin")

        # ✅ Normal user login
        user = users.find_one({"username": user_name})

        if user and check_password_hash(user["password"], user_password):
            
            return render_template("demo.html")

        return "Invalid username or password"

    return render_template("login.html")


# ------------------ REGISTER ------------------
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        user_name = request.form["username"]
        age = int(request.form["age"])
        user_password = request.form["password"]

        if user_name == ADMIN_USERNAME:
            return "This username is reserved"

        if users.find_one({"username": user_name}):
            return "Username already exists"

        users.insert_one({
            "username": user_name,
            "age": age,
            "password": generate_password_hash(user_password)
        })

        return redirect("/")

    return render_template("register.html")


# ------------------ ADMIN PAGE ------------------
@app.route("/admin")
def admin_page():

    # ✅ Correct MongoDB projection
    user_list = users.find(
        {},
        {"_id": 0, "username": 1, "age": 1}
    )

    return render_template("admin.html", users=user_list)


# ------------------ LOGOUT ------------------
@app.route("/logout")
def logout():
    return redirect("/")


# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)
