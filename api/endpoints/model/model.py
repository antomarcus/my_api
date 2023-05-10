import keras
import numpy as np
import pandas as pd

class model_Lead:
    def __init__(self) -> None:
        self.model = keras.models.load_model('/my_model')
    
    def preprocessing(self, data):
        df_test = pd.DataFrame(data, index=[0])
        # Convert the DataFrame to a NumPy arra
        return df_test
    
    def model_prediction(self, input_data):
        
        try:
            
            df = self.preprocessing(input_data)
            predictions = self.model.predict(df)
            predicted_labels = np.argmax(predictions, axis=1)

            for i in predicted_labels:
                if i== 0:
                    label = "Below_MAL"

                else:
                    label = "Above_MAL"

            prediction = {'label': label, "status": "OK"}

        except Exception as e:
             return {"status": "Error", "message": str(e)}
       
        return prediction
