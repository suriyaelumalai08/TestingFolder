from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    result=None

    if request.method == "POST":
        try:
            user_text = int(request.form['num1'])
            b=int(request.form['num2'])
            result=user_text+b
        except ValueError:
            result="invalid input" 
    return render_template("h.html",result=result)



if __name__ == "__main__":
    app.run(debug=True)
