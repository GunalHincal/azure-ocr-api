
# Azure OCR API

This project provides a REST API to extract text from images using Azure Computer Vision OCR. Users can upload images to this FastAPI-based API and receive the extracted text in JSON format.

## Features

*   **Support for JPEG and PNG formats:** The API supports images in JPEG and PNG formats.
*   **Automatic format conversion:** Images with unsupported modes (e.g., RGBA) are automatically converted to RGB.
*   **Resizing large images:** Very large images are automatically resized for optimal processing.
*   **Pillow integration:** Utilizes the powerful Pillow library for image processing.
*   **Azure OCR integration:** Leverages Azure Computer Vision OCR for fast and accurate text extraction.

## Requirements

*   Python 3.8 or above
*   Azure Computer Vision subscription key and endpoint
*   Python dependencies stored in the `requirements.txt` file.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/username/azure-ocr-api.git
    cd azure-ocr-api
    ```
    
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up the configuration:**
    *   Create a `config.py` file. This file stores your Azure credentials needed to connect to the Azure service.
    *   Add the following to `config.py`:

        ```python
        AZURE_ENDPOINT = "https://<your-endpoint>.cognitiveservices.azure.com/"
        AZURE_KEY = "<your-subscription-key>"
        ```
        
4.  **Run the API:**
    ```bash
    uvicorn main:app --reload
    ```

## API Endpoints

Here are the available API endpoints:

*   **Root endpoint:**
    *   URL: `/`
    *   Method: `GET`
    *   Description: Checks if the API is running.
    
*   **Text extraction endpoint:**
    *   **URL:** `/extract-text/`
    *   **Method:** `POST`
    *   **Body:** `multipart/form-data`
    *   **Description:** Upload an image file (uploaded with the `file` key).
    *   **Response:**
   
        ```json
        {"extracted_text": ["Extracted text line 1", "Extracted text line 2"]}
        ```
    *  **On Error:**
         ```json
        {"error": "Error message"}
        ```
        
        *  **Common Error Types:**
             *   `"Invalid Image Format"` if the uploaded image is not in JPEG or PNG format.
             *   `"Azure OCR API Error"` if there are issues with the Azure service.
             *   `"Internal Server Error"` for general server-side problems.

## Usage

Access the API documentation:
Open the following URL in your browser:
    ```
    http://127.0.0.1:8000/docs
    ```

### Example Test

You can test the API using the Swagger UI, which provides an easy-to-use graphical interface for testing endpoints.

#### Testing with Swagger UI

1. Start the API server:

   ``bash
   uvicorn main:app --reload
``

2.  Open your browser and navigate to:
    
    ```
    http://127.0.0.1:8000/docs
    ```
    
2.  Locate the POST /extract-text/ endpoint in the Swagger UI.
    
3.  Click the Try it out button.
    
4.  Upload an image file under the file parameter.
    
5.  Click Execute to send the request.
    
6.  View the response in the Responses section, where the extracted text will be displayed as JSON.
    

#### Testing with Postman

Alternatively, you can test the API using Postman.

1.  Open Postman and create a new POST request.
    
2.  Set the request URL to:
    
    ```
    http://127.0.0.1:8000/extract-text/
    ```
    
3.  In the Body tab, select form-data and add the following:
    
    -   **Key:** file (type: File)
        
    -   **Value:** Upload your image file (e.g., example.png).
        
4.  Click Send to make the request.
    

If successful, the response will contain the extracted text in JSON format.

#### Example cURL Command:


curl -X POST "http://127.0.0.1:8000/extract-text/" \
     -H "accept: application/json" \
     -F "file=@example.png"


## Docker (Optional)

You can use Docker to containerize and run the application. Here's a simple approach:

1.  **Create a Dockerfile:**
    
    ```
    FROM python:3.9-slim
    
    WORKDIR /app
    
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    COPY . .
    
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

    
2.  **Build the Docker image:**
    
    ```
    docker build -t azure-ocr-api .
    ```

    
3.  **Run the Docker container:**
    
    ```
    docker run -p 8000:8000 azure-ocr-api
    ```
    
    -   Now, you can access the API at http://localhost:8000.
        

## Deploy Link

This project is live and can be accessed here: [Render Deploy Link](https://azure-ocr-api.onrender.com/docs)

## Known Issues

-   **Unsupported Image Formats:** Only JPEG and PNG formats are supported. Must be 5mb or less.
    
-   **Large Images:** Very large images are resized automatically.
    

## Contribution

1.  Fork this repository.
    
2.  Create a new branch:
    
    ```
    git checkout -b feature/feature-name
    ```
    
3.  Make your changes and commit them:
    
    ```
    git commit -m "Added a new feature"
    ```    
    
4.  Push your branch:
    
    ```
    git push origin feature/feature-name
    ```
    
5.  Open a Pull Request.
    

## Follow Me for More Updates

Stay connected and follow me for updates on my projects, insights, and tutorials:

-  **LinkedIn:** **[Connect with me professionally to learn more about my work and collaborations](https://www.linkedin.com/in/gunalhincal)**
    
-   **Medium:** **[Check out my blog for articles on technology, data science, and more!](https://medium.com/@hincalgunal)**

Feel free to reach out or follow for more updates! 😊 Have Fun!



