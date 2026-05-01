from flask import Flask,render_template,request,session,redirect
from pymongo import MongoClient
import main2


app=Flask(__name__)

@app.route('/',methods=['GET',"POST"])
def index():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        data=main2.find_user(username)
        if data['username']==username and data['password']==password:
            return render_template('demo.html')
        return "filed"
    return render_template('home.html')
       
@app.route('/register',methods=['GET',"POST"])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        age=request.form['age']
        data={'username':username,'password':password,'age':age}
        main2.add_user(data)
        return 'successfuly'
    return render_template('register.html')


if __name__=='__main__':
    app.run(debug=True)




