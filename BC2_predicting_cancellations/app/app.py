import os
from pathlib import Path
import numpy as np
from flask import Flask, request, jsonify, render_template
from joblib import load
import pandas as pd

def create_df(dicti):

    transformed = {}
    for feature in dicti:
        if feature == 'MarketSegment':
            if dicti[feature] == 'Online TA':
                transformed['MarketSegment_Online TA']=1
            else:
                transformed['MarketSegment_Online TA']=0

        elif feature == 'CustomerType':
            if dicti[feature] == 'Transient':
                transformed['CustomerType_Transient']=1
                transformed['CustomerType_Transient-Party']=0 

            elif dicti[feature] == 'Transient-Party':
                transformed['CustomerType_Transient']=0
                transformed['CustomerType_Transient-Party']=1 
            else:
                transformed['CustomerType_Transient']=0
                transformed['CustomerType_Transient-Party']=0 


        elif feature == 'DepositType':
            if dicti[feature] == 'Non Refund':
                transformed['DepositType_Non Refund']=1
                transformed['DepositType_No Deposit']=0

            elif dicti[feature] == 'No Deposit':
                transformed['DepositType_Non Refund']=0
                transformed['DepositType_No Deposit']=1  

            else:
                transformed['DepositType_Non Refund']=0
                transformed['DepositType_No Deposit']=0       
        else:     
            transformed[feature]=dicti[feature]

    rearrange_cols =  ['LeadTime', 'TotalOfSpecialRequests', 'StaysInWeekNights', 'ADR',
       'ArrivalDateWeekNumber', 'Agent', 'ReservedRoomType',
       'DepositType_No Deposit', 'BookingChanges', 'AssignedRoomType',
       'Country', 'PreviousCancellations', 'Company', 'DistributionChannel',
       'DepositType_Non Refund', 'MarketSegment_Online TA',
       'ArrivalDateDayOfMonth', 'ArrivalDateMonth', 'CustomerType_Transient',
       'CustomerType_Transient-Party', 'RequiredCarParkingSpaces',
       'DaysInWaitingList', 'StaysInWeekendNights',
       'PreviousBookingsNotCanceled', 'Adults']
        
    new_obv_df = pd.DataFrame(transformed,index=[0])
    new_obv_df = new_obv_df[rearrange_cols]
    return new_obv_df

PROJECT_ROOT = Path(os.path.abspath('')).resolve()

app = Flask(__name__)  # Initialize the flask App
scaler = load(os.path.join(PROJECT_ROOT, 'models', 'scaler.joblib'))
model = load(os.path.join(PROJECT_ROOT, 'models', 'extra_tree.joblib'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    new_obv = {
            'LeadTime':int(request.form['lead']), 
            'TotalOfSpecialRequests':int(request.form['special_requests']),
            'StaysInWeekNights':int(request.form['week_in_stay']),
            'ADR':int(request.form['adr']),
            'ArrivalDateWeekNumber':int(request.form['week']),
            'Agent': int(request.form['agent']), 
            'ReservedRoomType':int(request.form['reserved_room']),
            'DepositType':request.form['type_of_deposit'],
            'BookingChanges':int(request.form['booking_changes']),
            'AssignedRoomType':int(request.form['assigned_room']),
            'PreviousCancellations':int(request.form['previous_cancel']),
            'Country':int(request.form['country']),
            'ArrivalDateMonth':int(request.form['month']),
            'MarketSegment':request.form['market_segment'],
            'ArrivalDateDayOfMonth':int(request.form['day']), 
            'Company':int(request.form['company']),
            'CustomerType':request.form['Customer_Type'],
            'RequiredCarParkingSpaces':int(request.form['parking_spaces']),
            'DaysInWaitingList':int(request.form['waiting_list']),
            'StaysInWeekendNights':int(request.form['weekend_stay']),
            'PreviousBookingsNotCanceled':int(request.form['previous_notcancel']), 
            'Adults':int(request.form['Adults']),
            'DistributionChannel':int(request.form['distribution_channel'])
            }
    new_obv_df = create_df(new_obv)
    new_obv_df = pd.DataFrame(scaler.transform(new_obv_df),columns=new_obv_df.columns)
    proba = round(model.predict_proba(new_obv_df)[0][1]*100,2)
    return render_template('index.html', prediction_text=proba)

if __name__ == "__main__":
    app.run(debug=True)

