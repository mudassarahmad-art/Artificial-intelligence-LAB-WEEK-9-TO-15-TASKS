from flask import Flask,render_template,request
import pandas as pd
import numpy as np
import pickle
app=Flask(__name__)
model=pickle.load(open("model.pkl","rb"))
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/predict",methods=["POST"])
def predict():
    featue=[float(x)for x in request.form.values()]
    fin=np.array([featue])
    pred=model.predict(fin)
    return render_template("index.html",pred="The predicted Price Is: {pred[0]}")
if __name__=="__main__":
    app.run(debug=True)
