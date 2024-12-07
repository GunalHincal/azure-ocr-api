# Azure OCR API

This project provides a **REST API** to extract text from images using **Azure Computer Vision OCR**. Users can upload images to this `FastAPI`-based API and receive the extracted text in JSON format.

## Features

-   **Support for JPEG and PNG formats**: The API supports images in JPEG and PNG formats.

-   **Automatic format conversion**: Images with unsupported modes (e.g., RGBA) are automatically converted to **RGB**.

-   **Resizing large images**: Very large images are automatically resized for optimal processing.

-   **Pillow integration**: Utilizes the powerful Pillow library for image processing.

-   **Azure OCR integration**: Leverages Azure Computer Vision OCR for fast and accurate text extraction.

## Requirements

-   Python 3.8 or above
-   Azure Computer Vision subscription key and endpoint

## Installation

1.  **Clone the repository**:
 
 _bash_      
`git clone https://github.com/username/azure-ocr-api.git
    cd azure-ocr-api` 
    
    
2.  **Install dependencies**:
    
    _bash_
    `pip install -r requirements.txt`
     
    
3.  **Set up the configuration**: 

Create a `config.py` file and add the following:
 
_python_ 
`AZURE_ENDPOINT = "https://<your-endpoint>.cognitiveservices.azure.com/"
    AZURE_KEY = "<your-subscription-key>"` 
    
    
5.  **Run the API**:
    
    _bash_
    `uvicorn main:app --reload` 
    
    
6.  **Access the API documentation**: 

Open the following URL in your browser:

_arduino_
    `http://127.0.0.1:8000/docs` 
    

## Usage

### API Endpoints

1.  **Root endpoint**:
    
    -   **URL**: `/`
    -   **Method**: GET
    -   **Description**: Checks if the API is running.
2.  **Text extraction endpoint**:
    
    -   **URL**: `/extract-text/`
    -   **Method**: POST
    -   **Body**: `multipart/form-data`
        -   An image file (uploaded with the `file` key).
   -   **Response**:

  _json_    
`{
          "extracted_text": ["Extracted text line 1", "Extracted text line 2"]
        }` 
        
   -  **On Error**:

_json_       
 `{
          "error": "Error message"
        }` 
        


## Example Test

You can test the API using the **Swagger UI**, which provides an easy-to-use graphical interface for testing endpoints.

### Testing with Swagger UI

1.  Start the API server:
    
    _bash_
    `uvicorn main:app --reload` 
    
2.  Open your browser and navigate to:
    
    arduino
    `http://127.0.0.1:8000/docs` 
    
3.  Locate the **`POST /extract-text/`** endpoint in the Swagger UI.

4.  Click the **`Try it out`** button.

5.  Upload an image file under the `file` parameter.

6.  Click **Execute** to send the request.

7.  View the response in the **Responses** section, where the extracted text will be displayed as JSON.

### Optional: Testing with Postman

Alternatively, you can test the API using **Postman**.

1.  Open Postman and create a new `POST` request.
2.  Set the request URL to:
    
    _vbnet_ 
    `http://127.0.0.1:8000/extract-text/` 
    
3.  In the **Body** tab, select **form-data** and add the following:

    -   Key: `file` (type: File)
    -   Value: Upload your image file (e.g., `example.png`).
 
4.  Click **Send** to make the request.
5.  If successful, the response will contain the extracted text in JSON format.


**Example cURL Command**:

_bash_
`curl -X POST "http://127.0.0.1:8000/extract-text/" \
-H "accept: application/json" \
-F "file=@example.png"`

## Known Issues

-   **Unsupported Image Formats**: Only JPEG and PNG formats are supported.

-   **Large Images**: Very large images are resized automatically.

## Contribution

1.  Fork this repository.
2.  Create a new branch:
    
_bash_
`git checkout -b feature/feature-name` 
    
3.  Make your changes and commit them:
    
_bash_
`git commit -m "Added a new feature"` 
    
4.  Push your branch:
    
_bash_
`git push origin feature/feature-name` 
    
5.  Open a **Pull Request**.

.
.
.
## Follow Me for More Updates

Stay connected and follow me for updates on my projects, insights, and tutorials:

-   **[LinkedIn](https://www.linkedin.com/in/gunalhincal)**: Connect with me professionally to learn more about my work and collaborations.
-   **[Medium](https://medium.com/@hincalgunal)**: Check out my blog for articles on technology, data science, and more!

Feel free to reach out or follow for more updates! 😊
Have Fun!