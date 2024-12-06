import streamlit as st
import pandas as pd
import numpy as np
import pickle  # For loading the RandomForestClassifier model

# Load the RandomForestClassifier model
with open('newmkc.pkl', 'rb') as file:
    saved_rf = pickle.load(file)

def predict(model, input_df):
    # Ensure the input DataFrame matches the model's expected feature format
    prediction_proba = model.predict_proba(input_df)[:, 1]  # Get the probability of class 1 (fraud)
    prediction = model.predict(input_df)  # Get the class prediction (0 or 1)
    
    st.write(f"Prediction Probability: {prediction_proba[0]}")  # For debugging
    return prediction[0]  # Return the prediction for the first instance

def run():
    st.sidebar.image("logo.webp", caption='Dept. of AI&ML, BIT Bangalore')
    st.title("Online Payments Fraud Detection System")
    st.sidebar.subheader('Under the Guidance of Dr. Jyothi D.G')

    # Input form
    get = st.selectbox("Transaction Type", ['CASH_OUT', 'CASH_IN', 'PAYMENT', 'TRANSFER', 'DEBIT'])
    type_mapping = {'CASH_OUT': 0, 'CASH_IN': 1, 'PAYMENT': 2, 'TRANSFER': 3, 'DEBIT': 4}
    Type = type_mapping[get]

    amount = st.number_input("Amount", value=0.0)
    oldbalanceOrg = st.number_input("Initial balance before the transaction", value=0.0)
    oldbalanceDest = st.number_input("Receiver's balance before the transaction", value=0.0)

    # Prepare input data
    input_dict = {
        'step':1,
        'type': Type,
        'amount': amount,
        'oldbalanceOrg': oldbalanceOrg,
        'oldbalanceDest': oldbalanceDest
    }
    input_df = pd.DataFrame([input_dict])

    st.sidebar.bar_chart(input_df)  # Display input data in the sidebar

    output = ""
    if st.button('Predict'):
        output = predict(model=saved_rf, input_df=input_df)
        if output == 1:
            output = 'Your Transaction is Fraudulent'
        elif output == 0:
            output = 'Your Transaction is Not Fraudulent'

    st.success(output)

run()
