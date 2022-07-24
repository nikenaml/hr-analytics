from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model_file = open('model_lgbm.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict the insurance cost based on user inputs
    and render the result to the html page
    '''
    avg_training_score, kpis_met, previous_year_rating, awards_won, education, no_of_trainings, length_of_service, age, recruitment_channel, department = [x for x in request.form.values()]

    data = []

    data.append(int(avg_training_score))

    if kpis_met == 'yes':
        data.extend([1])
    else:
        data.extend([0])

    data.append(int(previous_year_rating))

    if awards_won == 'yes':
        data.extend([1])
    else:
        data.extend([0])

    if education == 'below':
        data.extend([0])
    if education == 'bachelor':
        data.extend([1])
    if education == 'master':
        data.extend([2])

    data.append(int(no_of_trainings))

    data.append(int(length_of_service))


    if age == '20-30':
        data.extend([0])
    if age == '31-40':
        data.extend([1])
    if age == '41+':
        data.extend([2])

    # if gender == 'f':
    #     data.extend([0, 1])
    # else:
    #     data.extend([1, 0])

    if recruitment_channel == 'sourcing':
        data.extend([1, 0, 0])
    elif recruitment_channel == 'referred':
        data.extend([0, 1, 0])
    else:
        data.extend([0, 0, 1])

    if department == 'technology':
        data.extend([1, 0, 0, 0, 0, 0, 0, 0, 0])
    elif department == 'analytics':
        data.extend([0, 1, 0, 0, 0, 0, 0, 0, 0])
    elif department == 'sales_marketing':
        data.extend([0, 0, 1, 0, 0, 0, 0, 0, 0])
    elif department == 'rnd':
        data.extend([0, 0, 0, 1, 0, 0, 0, 0, 0])
    elif department == 'procurement':
        data.extend([0, 0, 0, 0, 1, 0, 0, 0, 0])
    elif department == 'operations':
        data.extend([0, 0, 0, 0, 0, 1, 0, 0, 0])
    elif department == 'finance':
        data.extend([0, 0, 0, 0, 0, 0, 1, 0, 0])
    elif department == 'legal':
        data.extend([0, 0, 0, 0, 0, 0, 0, 1, 0])
    else:
        data.extend([0, 0, 0, 0, 0, 0, 0, 0, 1])
    
    prediction = model.predict([data])
    is_promote = []
    if prediction[0] == True:
        is_promote.append('Get promotion')
    else:
        is_promote.append("Can't get promotion")

    return render_template('index.html', output=is_promote[0])


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()