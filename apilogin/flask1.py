from flask import Flask, request, redirect, url_for, session, render_template_string
import requests

app = Flask(__name__)
app.secret_key = "1a2b3c4d5e6f7g8h9i0j"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        r = requests.post(
            "http://127.0.0.1:8000/api/login",
            json={"username": username, "password": password}
        )

        if r.json().get("success"):
            session["logged_in"] = True
            return redirect(url_for("dashboard"))

        return "Login failed"

    return render_template_string("""
        <h2>LOGIN</h2>
        <form method="post">
            <input name="username" placeholder="username"><br><br>
            <input name="password" type="password" placeholder="password"><br><br>
            <button type="submit">Login</button>
        </form>
    """)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return "<h2>Welcome, you are verified.</h2>"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
