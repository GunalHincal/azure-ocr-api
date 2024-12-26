# REST API code repository

import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import config
import time
import io
from PIL import Image, UnidentifiedImageError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI application
app = FastAPI()

# Azure Computer Vision client
computervision_client = ComputerVisionClient(
    config.AZURE_ENDPOINT,
    CognitiveServicesCredentials(config.AZURE_KEY)
)

def process_image(contents):
    """
    Processes the uploaded image to ensure it is in the correct format and size.

    Args:
        contents (bytes): The raw image content.

    Returns:
        BytesIO: Processed image in JPEG format.
    """
    try:
        image = Image.open(io.BytesIO(contents))
        logger.info(f"Original Image Mode: {image.mode}, Format: {image.format}, Size: {image.size}")

        if image.mode == "RGBA":
            image = image.convert("RGB")
            logger.info("Converted RGBA to RGB.")
        elif image.mode not in ["RGB", "L"]:
            image = image.convert("RGB")
            logger.info("Converted image to RGB.")

        if max(image.size) > 2000:
            new_size = (2000, 2000) if image.size[0] > image.size[1] else (image.size[0], 2000)
            image.thumbnail(new_size, Image.LANCZOS)
            logger.info(f"Resized image to {image.size}.")

        image_stream = io.BytesIO()
        image.save(image_stream, format="JPEG")
        image_stream.seek(0)
        logger.info("Image successfully processed and converted to JPEG.")
        return image_stream

    except UnidentifiedImageError:
        raise ValueError("The uploaded file is not a valid image.")
    except Exception as e:
        logger.error(f"Error during image processing: {e}")
        raise

# Root route: Check if the API is running
@app.get("/")
def read_root():
    """
    Root route: Checks if the API is running.

    Returns:
        dict: A message indicating the API is running and suggests using /extract-text endpoint.
    """
    return {"message": "API is running! Use /extract-text to upload an image."}

# Main route: Upload an image and extract text
@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    """
    Endpoint to extract text from an image.

    This endpoint accepts an image file and uses the Azure Computer Vision OCR service to extract text.

    Args:
        file (UploadFile): The image file to be uploaded.

    Returns:
        dict: A JSON object containing the extracted text. 
              If the process fails, it returns an error message.
    """
    try:
        contents = await file.read()
        logger.info(f"Uploaded file type: {file.content_type}")

        if file.content_type not in ["image/jpeg", "image/png"]:
            return JSONResponse(
                content={"error": "Unsupported file type. Only JPEG and PNG formats are supported."},
                status_code=400  # Bad Request
            )

        image_stream = process_image(contents)

        # Send the image to Azure OCR
        results = computervision_client.read_in_stream(image_stream, raw=True)
        operation_location = results.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Retrieve results
        read_result = computervision_client.get_read_result(operation_id)
        while read_result.status not in ["succeeded", "failed"]:
            time.sleep(1)
            read_result = computervision_client.get_read_result(operation_id)

        if read_result.status == "succeeded":
            extracted_text = [line.text for page in read_result.analyze_result.read_results for line in page.lines]
            return JSONResponse(
                content={"extracted_text": extracted_text},
                status_code=200  # OK
            )

        return JSONResponse(
            content={"error": "Text extraction failed."},
            status_code=400  # Bad Request
        )

    except ValueError as ve:
        logger.error(str(ve))
        return JSONResponse(
            content={"error": str(ve)},
            status_code=422  # Unprocessable Entity
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JSONResponse(
            content={"error": "An unexpected error occurred."},
            status_code=500  # Internal Server Error
        )



    