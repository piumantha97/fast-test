
from fastapi import FastAPI
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from mobile import Mobile
import numpy as np
import pickle
import pandas as pd
import joblib
from fastapi import HTTPException
# 2. Create the app object
app = FastAPI()
# pickle_in = open("rf_model.pkl","wb")
# classifier=pickle.load(pickle_in)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, replace with your frontend's actual origin
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods
    allow_headers=["*"],  # This allows all headers
)



# Save the model
# joblib.dump(classifier, "rf_model.joblib")



# Load the model
# classifier = joblib.load("mpr1.joblib")

with open("mpr1.joblib", "rb") as file:
    classifier = joblib.load(file)


# Brand mapping
brand_mapping = {
    1: "Samsung",
    2: "Huawei",
    3: "Apple",
    4: "Redmi",
    5: "Vivo",
    6: "Oppo",
    7: "Nokia",
    0: "Other",
}


@app.get("/")
def index():
    return {"Hello": "World"}




# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Krish Youtube Channel': f'{name}'}




# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
def predict_mobile(data:Mobile):
    try:
        print(data.dict())

        # Convert the Pydantic model to a dictionary
        data_dict = data.dict()

    # Extract values from the dictionary
        features = [
            data_dict['Gender'],
            data_dict['Age'],
            data_dict['Education'],
            data_dict['Occupation'],
            data_dict['District'],
            data_dict['CameraSatisfaction'],
            data_dict['MemorySatisfaction'],
            data_dict['PerformanceSatisfaction'],
            data_dict['BatterySatisfaction'],
            data_dict['spend_amount'],
            data_dict['Education_purpose'],
            data_dict['Entertaintment_purpose'],
            data_dict['Gaming_purpose'],
            data_dict['Occupation_purpose'],
            data_dict['Photography_purpose'],
            data_dict['Socializing_purpose']
        ]
    # print(classifier.predict([[variance,skewness,curtosis,entropy]]))
        # prediction = classifier.predict([[Gender,Age,Education,Occupation,District,CameraSatisfaction,MemorySatisfaction,PerformanceSatisfaction,BatterySatisfaction,spend_amount,Education_purpose,Entertaintment_purpose,Gaming_purpose,Occupation_purpose,Photography_purpose,Socializing_purpose]])

        print("Input Features:", features)

    # Make a prediction
        # prediction = classifier.predict([features])
        probabilities = classifier.predict_proba([features])[0]
        #  return {'prediction': prediction.tolist()} 
        # Create a list of tuples containing (brand_id, probability)
        brand_probabilities = list(enumerate(probabilities))

        # Sort the brands based on probabilities in descending order
        sorted_brands = sorted(brand_probabilities, key=lambda x: x[1], reverse=True)

        # Map the numeric prediction to the brand names
        ranked_brands = [brand_mapping.get(brand_id, "Unknown") for brand_id, _ in sorted_brands]

        return {'prediction': ranked_brands}
#    return {'prediction': [predicted_brand]}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    import os
    # Use the environment variable PORT, default to 8000 if not set
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
