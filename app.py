from tensorflow.keras.models import load_model
from flask import Flask, request, render_template
from tensorflow.keras.models import model_from_json
from flask_cors import cross_origin
# import pandas as pd
# from sklearn.preprocessing import StandardScaler


app = Flask(__name__)

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")

loaded_model.save('model.hdf5')
loaded_model = load_model('model.hdf5')


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        gender_Male = int(request.form["gender"])

        SeniorCitizen_1 = int(request.form["SeniorCitizen"])

        Partner_Yes = int(request.form["Partner"])

        Dependents_Yes = int(request.form["Dependents"])

        tenure = float(request.form['tenure'])

        PhoneService_Yes = int(request.form["PhoneService"])

        MultipleLines = request.form["MultipleLines"]
        if MultipleLines == 'yes':
            MultipleLines_Nophoneservice = 0
            MultipleLines_Yes = 1
        elif MultipleLines == 'no':
            MultipleLines_Nophoneservice = 0
            MultipleLines_Yes = 0
        else:
            MultipleLines_Nophoneservice = 1
            MultipleLines_Yes = 0

        InternetService = request.form["InternetService"]
        if InternetService == 'fibre optic':
            InternetService_Fiberoptic= 1
            InternetService_No = 0
        elif InternetService == 'no':
            InternetService_Fiberoptic = 0
            InternetService_No = 1
        else:
            InternetService_Fiberoptic = 0
            InternetService_No = 0

        OnlineSecurity = request.form["OnlineSecurity"]
        if OnlineSecurity == 'yes':
            OnlineSecurity_Nointernetservice= 0
            OnlineSecurity_Yes = 1
        elif OnlineSecurity == 'no':
            OnlineSecurity_Nointernetservice = 0
            OnlineSecurity_Yes = 0
        else:
            OnlineSecurity_Nointernetservice = 1
            OnlineSecurity_Yes = 0

        OnlineBackup = request.form["OnlineBackup"]
        if OnlineBackup == 'yes':
            OnlineBackup_Nointernetservice= 0
            OnlineBackup_Yes = 1
        elif OnlineBackup == 'no':
            OnlineBackup_Nointernetservice = 0
            OnlineBackup_Yes = 0
        else:
            OnlineBackup_Nointernetservice = 1
            OnlineBackup_Yes = 0

        DeviceProtection = request.form["DeviceProtection"]
        if DeviceProtection == 'yes':
            DeviceProtection_Nointernetservice= 0
            DeviceProtection_Yes = 1
        elif DeviceProtection == 'no':
            DeviceProtection_Nointernetservice = 0
            DeviceProtection_Yes = 0
        else:
            DeviceProtection_Nointernetservice = 1
            DeviceProtection_Yes = 0

        TechSupport = request.form["TechSupport"]
        if TechSupport == 'yes':
            TechSupport_Nointernetservice= 0
            TechSupport_Yes = 1
        elif TechSupport == 'no':
            TechSupport_Nointernetservice = 0
            TechSupport_Yes = 0
        else:
            TechSupport_Nointernetservice = 1
            TechSupport_Yes = 0


        StreamingTV = request.form["StreamingTV"]
        if StreamingTV == 'yes':
            StreamingTV_Nointernetservice= 0
            StreamingTV_Yes = 1
        elif StreamingTV == 'no':
            StreamingTV_Nointernetservice = 0
            StreamingTV_Yes = 0
        else:
            StreamingTV_Nointernetservice = 1
            StreamingTV_Yes = 0

        StreamingMovies = request.form["StreamingMovies"]
        if StreamingMovies == 'yes':
            StreamingMovies_Nointernetservice= 0
            StreamingMovies_Yes = 1
        elif StreamingMovies == 'no':
            StreamingMovies_Nointernetservice = 0
            StreamingMovies_Yes = 0
        else:
            StreamingMovies_Nointernetservice = 1
            StreamingMovies_Yes = 0

        Contract = request.form["Contract"]
        if Contract == 'One year':
            Contract_Oneyear= 1
            Contract_Twoyear= 0
        elif Contract == 'Two year':
            Contract_Oneyear = 0
            Contract_Twoyear = 1
        else:
            Contract_Oneyear = 0
            Contract_Twoyear = 0

        PaperlessBilling_Yes = int(request.form["PaperlessBilling"])

        PaymentMethod = request.form["PaymentMethod"]
        if PaymentMethod == 'Electronic check':
            PaymentMethod_Creditcard = 0
            PaymentMethod_Electroniccheck= 1
            PaymentMethod_Mailedcheck=0
        elif PaymentMethod == 'Mailed check':
            PaymentMethod_Creditcard = 0
            PaymentMethod_Electroniccheck = 0
            PaymentMethod_Mailedcheck = 1
        elif PaymentMethod == 'Bank transfer (automatic)':
            PaymentMethod_Creditcard = 0
            PaymentMethod_Electroniccheck = 0
            PaymentMethod_Mailedcheck = 0
        else:
            PaymentMethod_Creditcard = 1
            PaymentMethod_Electroniccheck = 0
            PaymentMethod_Mailedcheck = 0


        MonthlyCharges = float(request.form["MonthlyCharges"])

        TotalCharges = float(request.form["TotalCharges"])




        prediction = loaded_model.predict([[tenure, MonthlyCharges, TotalCharges, gender_Male, SeniorCitizen_1, Partner_Yes, Dependents_Yes, PhoneService_Yes,
                                            MultipleLines_Nophoneservice,MultipleLines_Yes,InternetService_Fiberoptic,InternetService_No,OnlineSecurity_Nointernetservice,
                                            OnlineSecurity_Yes,OnlineBackup_Nointernetservice,OnlineBackup_Yes,DeviceProtection_Nointernetservice,DeviceProtection_Yes,
                                            TechSupport_Nointernetservice,TechSupport_Yes,StreamingTV_Nointernetservice,StreamingTV_Yes,StreamingMovies_Nointernetservice,
                                            StreamingMovies_Yes, Contract_Oneyear,Contract_Twoyear,PaperlessBilling_Yes,PaymentMethod_Creditcard,PaymentMethod_Electroniccheck,PaymentMethod_Mailedcheck]])

        if prediction==0:
            output="This customer may churn(leave)"
        else:
            output="This customer may continue"

        return render_template('home.html', prediction_text="{} ".format(output))

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
