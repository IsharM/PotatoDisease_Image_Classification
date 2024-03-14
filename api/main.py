from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()
MODEL = tf.keras.models.load_model("saved_models/1")
CLASSES = ['Early_blight', 'Late_blight', 'Healthy']


@app.get("/ping")
async def ping():
    return "API, is active."

def read_file_as_image(data) -> np.ndarray:
    try:
        image =np.array(Image.open(BytesIO(data)))  # data in-memory binary data , converted to Bytes
    except Exception as e:
        print(f"Exception from read_file_as_image, {e}")
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    try:
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)

        # predictions = MODEL.predict(img_batch)

        # predicted_class = CLASSES[np.argmax(predictions[0])]    # 0, as it returns as batch
        # confidence = np.max(predictions[0])
    except Exception as e:
         print(f"Exception from predict, {e}")

    return {
        'class' : predicted_class,
        'confidence' : confidence
    }


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)


