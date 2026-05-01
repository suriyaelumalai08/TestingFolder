from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("n.html")

@app.route("/add", methods=["POST"])
def add():
    try:
        num1 = int(request.form.get("num1"))
        num2 = int(request.form.get("num2"))
        return str(num1 + num2)
    except:
        return "Invalid input", 400

if __name__ == "__main__":
    app.run(debug=True)
