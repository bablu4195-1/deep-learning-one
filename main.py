from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import tensorflow as tf
import numpy as np
from PIL import Image
import pillow_heif  # Register HEIC support with Pillow
pillow_heif.register_heif_opener()
import io
import os
import traceback

app = FastAPI()

# Load the pre-trained model
model = tf.keras.models.load_model('my_digit_reader.keras')

# Create the frontend directory if it doesn't exist
os.makedirs("frontend", exist_ok=True)

# Mount the frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Receives an image file, preprocesses it, and returns the predicted digit.
    """
    try:
        # Debug: Log file info
        print(f"Received file: {file.filename}, Content-Type: {file.content_type}")
        
        # Read the image file
        contents = await file.read()
        print(f"File size: {len(contents)} bytes")
        
        if len(contents) == 0:
            return JSONResponse(content={"error": "Empty file received"}, status_code=400)
        
        # Check if content type is an image
        if file.content_type and not file.content_type.startswith('image/'):
            return JSONResponse(content={"error": f"Invalid file type: {file.content_type}. Please upload an image."}, status_code=400)
        
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
        error_trace = traceback.format_exc()
        print(f"Error in predict endpoint: {error_trace}")
        return JSONResponse(content={"error": str(e), "traceback": error_trace}, status_code=500)

# Serve the index.html file at the root
@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')
