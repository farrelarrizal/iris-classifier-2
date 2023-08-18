import streamlit as st
from PIL import Image
import requests

# header images
image = Image.open('assets/header-iris.png')
st.image(image)
st.title("Iris Classifier App")
st.markdown('by: Farrel Arrizal | Pacmann Batch July 2023')
st.divider()
st.subheader('Just type the value. Then, click the Predict button to get the result :sunglasses:')

# form input
with st.form("iris-app-form"):
    sepal_length =  st.number_input("Sepal Length", help="0.5")
    sepal_width =  st.number_input("Sepal Width", help="0.2")
    petal_length =  st.number_input("Petal Length", help="0.3")
    petal_width =  st.number_input("Petal Width", help="0.1")

    # submit button
    submitted = st.form_submit_button("Predict")

    # check if button clicked
    if submitted:
        # post data
        data = {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        }

        # post request
        response = requests.post('http://backend:8000/predict', json=data)

        # get response
        result = response.json()

        # check response
        if result['code'] == 200:
            messages = "The flower is " + result['prediction'] + " Iris"
            st.success(messages)
            # st.write(messages)

        else:
            st.error(result['messages'])
        
