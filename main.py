# REST API kodlarımızı tutuyoruz

from fastapi import FastAPI, File, UploadFile
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import config
import time
import io
from PIL import Image, UnidentifiedImageError

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
        # Dosyayı oku ve türünü kontrol et
        contents = await file.read()
        print(f"Uploaded file type: {file.content_type}")

        # Görüntüyü Pillow ile aç ve gerekirse dönüştür
        try:
            image = Image.open(io.BytesIO(contents))
            print(f"Original Image Mode: {image.mode}") # Görselin modunu yazdır
            print(f"Image Format: {image.format}")
            print(f"Image Size: {image.size}")  

            # Görseli uygun bir moda dönüştür
            if image.mode not in ["RGB", "L", "P"]:  # Eğer uyumsuz bir mod varsa
                if image.mode == "RGBA":
                    # Transparan pikselleri beyaz arka plan ile doldur
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    image = Image.alpha_composite(background, image)
                else:
                    # Diğer modları RGB'ye dönüştür
                    image = image.convert("RGB")
            
            # Gerekirse yeniden boyutlandır
            if max(image.size) > 2000:  # Görsel çok büyükse yeniden boyutlandır
                new_size = (2000, 2000) if image.size[0] > image.size[1] else (image.size[0], 2000)
                image.thumbnail(new_size, Image.ANTIALIAS)
            
            # Görüntüyü JPEG formatına kaydet
            image_stream = io.BytesIO()
            image.save(image_stream, format="JPEG")
            image_stream.seek(0)  # Stream'in başına dön
        except UnidentifiedImageError:
            return {"error": "The uploaded file is not a valid image."}

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
    




