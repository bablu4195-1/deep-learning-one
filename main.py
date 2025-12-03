from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Load the pre-trained model
model = tf.keras.models.load_model('my_digit_reader.keras')

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Receives an image file, preprocesses it, and returns the predicted digit.
    """
    try:
        # Read the image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('L')  # Convert to grayscale

        # Resize to 28x28
        image = image.resize((28, 28))

        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0

        # Reshape for the model
        image_array = image_array.reshape(1, 28, 28, 1)

        # Make a prediction
        prediction = model.predict(image_array)
        predicted_class = int(np.argmax(prediction, axis=1)[0])

        return JSONResponse(content={"prediction": predicted_class})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
