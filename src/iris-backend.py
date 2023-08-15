# import library
from fastapi import FastAPI
from fastapi import Request
import pickle
import uvicorn

# init app
app = FastAPI()

# check status [GET]
@app.get("/")
def hello():
    return "Hi there, Your API is UP!"


# load model function 
def load_model():
    # load model
    with open('model/iris-classifier.pkl', 'rb') as file:
        model = pickle.load(file)
    return model


# check model with api [GET]
@app.get("/check-model")
def check_model():
    # load model
    try:
        model = load_model()
        response = {
            "code": 200,
            "messages": "Model is ready!"
        }
    except Exception as e:
        response = {
            "code": 404,
            "messages": "Model is not ready! please check your path or model",
            "error": str(e)
        }
    return response


# predict with api [POST]
@app.post("/predict")
async def predict(request: Request):
    # get data from request
    # sepal_length, sepal_width, petal_length, petal_width
    data = await request.json()

    sepal_length = data['sepal_length']
    sepal_width = data['sepal_width']
    petal_length = data['petal_length']
    petal_width = data['petal_width']
    
    # load model & label
    model = load_model()
    label = ['setosa', 'versicolor', 'virginica']


    # validation
    if sepal_length < 0 or sepal_width < 0 or petal_length < 0 or petal_width < 0:
        response = {
            "code": 404,
            "messages": "Failed your input must greater than 0!"
        }
        return response
    
    
    # predict
    try:
        prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        # print(prediction)
        response = {
            "code": 200,
            "messages": "Success",
            "prediction": label[prediction[0]]
        }
    except:
        response = {
            "code": 404,
            "messages": "Failed"
        }

    # return response
    return response

# run app
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)