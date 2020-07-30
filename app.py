from flask import Flask, jsonify, render_template,request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('cleaned.csv')

df = df.drop(columns=['Week Start','Cases - Cumulative','Percent Tested Positive - Weekly','Deaths - Cumulative','Death Rate - Cumulative',
       'Population','Percent Tested Positive - Cumulative','Test Rate - Weekly','Tests - Cumulative','Test Rate - Cumulative','Case Rate - Cumulative','Week End','Week Number','Test Rate - Cumulative','Row ID','ZIP Code Location', 'ZIP Code'])

#Fix Column Names
df.columns = df.columns.str.strip().str.lower().str.replace('-', '').str.replace(' ', '_').str.replace('__', '_')


X = df.drop('deaths_weekly', axis = 1)
y = df['deaths_weekly'].values.reshape(-1, 1)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

#======================================================
# Flask app
#======================================================
app = Flask(__name__)

@app.route("/",methods=['POST', 'GET'])
def main():
#https://stackoverflow.com/questions/56934303/assign-a-variable-from-html-input-to-python-flask  
    try:
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        wcases = int(request.form.get('weeklycases'))
        wcaserate = int(request.form.get('weeklycaserate'))
        wtests = int(request.form.get('weeklytests'))
        wdeathrate = float(request.form.get('weeklydeathrate'))
    except:
        state = "Null"
        zipcode = "0"
        wcases = 0
        wcaserate = 0
        wtests = 0
        wdeathrate = 0.0
    global output 
    output=[wcases,wcaserate,wtests,wdeathrate]
    

    from sklearn.preprocessing import StandardScaler

    X_test =output

    X_test =np.asarray(X_test)
    X_test =X_test.reshape(1,-1)

    predictions = model.predict(X_test)

    return render_template("index.html",output=output, predictions=predictions,state=state,zipcode=zipcode)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    app.run(debug=True)