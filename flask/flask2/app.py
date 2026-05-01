from flask import Flask, request, render_template, redirect, session, jsonify
import joblib

app = Flask(__name__)
app.secret_key = 'su2ri00ya4'

model = joblib.load("web_model.joblib")


@app.route('/', methods=['GET', 'POST'])
def Home_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'suriya' and password == "123":
            session['username'] = username
            return redirect('/predict')
        else:
            return "Invalid credentials"

    return render_template('home.html')


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "username" not in session:
        return redirect("/")

    # Page load
    if request.method == "GET":
        return render_template("first.html")

    # AJAX prediction
    data = request.get_json(force=True)

    features = [[
        float(data["sepal_length"]),
        float(data["sepal_width"]),
        float(data["petal_length"]),
        float(data["petal_width"])
    ]]

    prediction = model.predict(features)

    label_map = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
    }

    pred_index = int(prediction[0])
    result = label_map[pred_index]

    return jsonify({
    "result": result
    })



if __name__ == "__main__":
    app.run(debug=True)
