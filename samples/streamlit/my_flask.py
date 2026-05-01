from flask import Flask, jsonify,render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_user():
    return jsonify({'username':'suriya','role':'python'})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
