import pickle as pk
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

loaded_model = pk.load(open("svm-model.pkl", 'rb'))

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/obesity", )
def obesity():
   return render_template('obesity.html')
    
@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        gender = request.form["gender"]
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        overWeight = request.form["overWeight"]
        caloric = request.form["caloric"]
        vegetables = request.form["vegetables"]
        mealsDaily = request.form["mealsDaily"]
        betweenMeals = request.form["betweenMeals"]
        smoke = request.form["smoke"]
        water = request.form["water"]
        monitor = request.form["monitor"]
        physicalActivity = request.form["physicalActivity"]
        devices = request.form["devices"]
        alcohol = request.form["alcohol"]
        transportation = request.form["transportation"]
        
        result = predictor(gender, age, height, weight, overWeight, caloric, vegetables, mealsDaily, betweenMeals, smoke, water, monitor, physicalActivity, devices, alcohol, transportation)
        if int(result) == 0:
            prediction = 'Insufficient Weight'
            suggestion = """Eat frequent, small meals throughout the day to increase calorie intake.
Choose foods that are high in healthy fats, proteins, and carbohydrates such as nuts, avocado, whole grains, and lean meats.
Incorporate strength training exercises into your fitness routine to build muscle mass and improve overall health."""
        elif int(result) == 1:
            prediction = 'Normal Weight'
            suggestion = """
            Eat a balanced diet that includes a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats.
Limit processed foods and sugary drinks.
Engage in regular physical activity, aiming for at least 150 minutes of moderate exercise per week.
            """
        elif int(result) == 2:
            prediction = 'Obesity Type I'
            suggestion = """Focus on portion control and consuming fewer calories.
Incorporate more fruits, vegetables, and lean proteins into your diet.
Increase physical activity, aiming for at least 150-300 minutes of moderate exercise per week."""
        elif int(result) == 3:
            prediction = 'Obesity Type II'
            suggestion = """Work with a healthcare professional to develop a personalized weight loss plan.
Eat a balanced diet with plenty of fruits, vegetables, whole grains, and lean proteins.
Engage in regular physical activity, aiming for at least 150-300 minutes of moderate exercise per week."""
        elif int(result) == 4:
            prediction = 'Obesity Type III'
            suggestion = """Work closely with a healthcare professional to develop a personalized weight loss plan.
Eat a balanced diet with plenty of fruits, vegetables, whole grains, and lean proteins.
Engage in regular physical activity, aiming for at least 300 minutes of moderate exercise per week."""
        elif int(result) == 5:
            prediction = 'Overweight Level I'
            suggestion = """Focus on portion control and consuming fewer calories.
Incorporate more fruits, vegetables, and lean proteins into your diet.
Increase physical activity, aiming for at least 150-300 minutes of moderate exercise per week."""
        elif int(result) == 6:
            prediction = 'Overweight Level II'
            suggestion = """Work with a healthcare professional to develop a personalized weight loss plan.
Eat a balanced diet with plenty of fruits, vegetables, whole grains, and lean proteins.
Engage in regular physical activity, aiming for at least 300 minutes of moderate exercise per week."""
        else: 
            prediction = 'Prediction Error'
        
        genderText = (lambda: "Female" if gender == 1 else "Male")()
        return render_template("result.html", prediction = prediction, gender = genderText, age = age, weight = weight, height = height, suggestion = suggestion)
    else:
        return render_template("index.html")

def predictor(gender, age, height, weight, overweight, caloric, vegetables, mealsDaily, betweenMeals, smoke, water, monitor, physicalActivity, devices, alcohol, transportation):
    new_data = [[gender, age, height, weight, overweight, caloric, vegetables, mealsDaily, betweenMeals, smoke, water, monitor, physicalActivity, devices, alcohol, transportation]]
    new_data_df = pd.DataFrame(new_data, columns=['Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight', 'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS'])
    predicted_label = loaded_model.predict(new_data_df)
    return predicted_label
