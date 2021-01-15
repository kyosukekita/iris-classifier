from flask import Flask, request, redirect, render_template, url_for,jsonify, Blueprint
from flask_login import LoginManager,login_user, logout_user, login_required
from user import User #https://liginc.co.jp/415333
import numpy as np
import tensorflow as tf
from tensorflow.compat.v1.keras.backend import set_session
from tensorflow.compat.v1.keras.models import load_model

app=Flask(__name__)


#---login,logoutを設定---
app.secret_key="secret key" #セッションを使うためにシークレットキーが必要
login_manager=LoginManager()
login_manager.init_app(app)

@app.route('/', methods=['GET'])
def form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = User.User()
    login_user(user)
    return redirect(url_for('iris'))


#---モデルを踏み込む---
global sess
global graph
model=tf.keras.models.load_model("iris_model.h5")
model._make_predict_function()
graph=tf.compat.v1.get_default_graph()
tf.compat.v1.set_random_seed(200)


#---モデルを実行する---
def model_run(data):
    data=data[np.newaxis,:]
    
    with graph.as_default():
        session=tf.keras.backend.get_session()
        init=tf.global_variables_initializer()
        session.run(init)
        ans=int(model.predict_classes(data))

    if ans==0:
        return "Setosa"
    elif ans==1:
        return "Versicolor"
    else:
        return "Virginica"


#----------------------
@app.route("/iris", methods=["GET"])
@login_required
def home():
    return render_template("iris.html")

@login_manager.user_loader
def load_user(user_id):
        return User.User()

@app.route("/iris", methods=["POST"])
def iris():

    sepal_length=float(request.form.get("seplen"))
    sepal_width=float(request.form.get("sepwid"))
    petal_length=float(request.form.get("petlen"))
    petal_width=float(request.form.get("petwid"))

    if sepal_length and sepal_width and petal_length and petal_width:
        data_list=[sepal_length, sepal_width, petal_length, petal_width]
        data=np.array(data_list)
        iris_class=model_run(data)
        return jsonify({'output':"Your iris is "+iris_class})
    
    return jsonify({"error":"Missing data"})

#----------------------
app.run(debug=True, port="8080")


"""
@app.route("/result", methods=["POST"])
def result():
    message="Your iris is ..."

    sepal_length=float(request.form["seplen"])
    sepal_width=float(request.form["sepwid"])
    petal_length=float(request.form["petlen"])
    petal_width=float(request.form["petwid"])

    data_list=[sepal_length, sepal_width, petal_length, petal_width]
    data=np.array(data_list)
    iris_class=model_run(data)

    return render_template("result.html", message=message, iris_class=iris_class, title="result")
"""