# REST API kodlarımızı tutuyoruz

from fastapi import FastAPI, File, UploadFile
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import config
import time  # Hata almamak için time modülü import edildi
import io  # Bytes'ı akışa çevirmek için gerekli

# FastAPI uygulaması
app = FastAPI()

# Azure Computer Vision istemcisi
computervision_client = ComputerVisionClient(
    config.AZURE_ENDPOINT,
    CognitiveServicesCredentials(config.AZURE_KEY)
)

# Ana rota: API'nin çalıştığını kontrol etmek için
@app.get("/")
def read_root():
    """
    Ana rota: API'nin çalıştığını kontrol eder.

    Returns:
        dict: Bir mesaj döndürür ve `/extract-text/` endpoint'ini kullanmanız gerektiğini belirtir.
    """
    return {"message": "API is running! Use /extract-text to upload an image."}

# Ana rota: Görüntü yükle ve metin çıkar
@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    """
    Görüntüden metin çıkarma işlemi yapan endpoint.

    Bu endpoint, bir görüntü dosyasını alır ve Azure Computer Vision OCR servisini kullanarak
    içindeki metni çıkartır.

    Args:
        file (UploadFile): Yüklenmesi gereken görüntü dosyası.

    Returns:
        dict: Çıkarılan metinleri içeren bir JSON objesi. 
              Eğer işlem başarısız olursa hata mesajı döner.
    """
    try:
        # Görsel türünü kontrol et
        print(f"Uploaded file type: {file.content_type}")  # Ör: image/jpeg
        if file.content_type not in ["image/jpeg", "image/png"]:
            return {"error": "Unsupported file type. Please upload a JPEG or PNG image."}


        # Dosyayı oku
        contents = await file.read()
        print(type(contents))  # Tür kontrolü (bytes olmalı)

        # Bytes verisini Pillow ile işleme ve format dönüştürme (isteğe bağlı)
        from PIL import Image
        image = Image.open(io.BytesIO(contents))
        image.save("converted_image.jpg", format="JPEG")  # JPEG formatına dönüştür

        # Dönüştürülmüş dosyayı tekrar oku
        with open("converted_image.jpg", "rb") as f:
            contents = f.read()

        # Bytes verisini bir akışa dönüştür
        image_stream = io.BytesIO(contents)

        # Azure OCR için görüntü gönder
        results = computervision_client.read_in_stream(image_stream, raw=True)
        operation_location = results.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Sonuçları al
        read_result = computervision_client.get_read_result(operation_id)
        while read_result.status not in ["succeeded", "failed"]:
            time.sleep(1)
            read_result = computervision_client.get_read_result(operation_id)

        # Metin sonuçlarını işleme
        if read_result.status == "succeeded":
            extracted_text = []
            for page in read_result.analyze_result.read_results:
                for line in page.lines:
                    extracted_text.append(line.text)
            return {"extracted_text": extracted_text}

        return {"error": "Text extraction failed"}
    except Exception as e:
        # Hata durumunda, detaylı hata mesajını döndürür
        print(f"Error Details: Endpoint={config.AZURE_ENDPOINT}, Key={config.AZURE_KEY}")
        print(f"Raw Error: {e}")
        return {"error": f"An error occurred: {str(e)}"}

    

    

