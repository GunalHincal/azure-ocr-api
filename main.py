# REST API kodlarımızı tutuyoruz

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
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
        if file.content_type not in ["image/jpeg", "image/png"]:
            return JSONResponse(
                content={"error": "Unsupported file type. Please upload a JPEG or PNG image."},
                status_code=400  # Bad Request
            )

        # Görüntüyü Pillow ile aç ve gerekirse dönüştür
        try:
            image = Image.open(io.BytesIO(contents))
            print(f"Original Image Mode: {image.mode}")
            print(f"Image Format: {image.format}")
            print(f"Image Size: {image.size}")

            # Görseli uygun bir moda dönüştür
            if image.mode == "RGBA":
                background = Image.new("RGB", image.size, (255, 255, 255))  # Transparan pikselleri beyaz arka plan ile doldur
                # Transparan pikselleri beyaz arka plan ile doldur
                image = Image.alpha_composite(background, image)
                print("Converted RGBA to RGB with white background.")
            elif image.mode not in ["RGB", "L"]:
                # Diğer modları RGB'ye dönüştür
                image = image.convert("RGB")
                print("Converted image to RGB.")
            
            # Gerekirse yeniden boyutlandır
            if max(image.size) > 2000:  # Görsel çok büyükse yeniden boyutlandır
                new_size = (2000, 2000) if image.size[0] > image.size[1] else (image.size[0], 2000)
                image.thumbnail(new_size, Image.LANCZOS)
                print(f"Resized image to {image.size}.")
            
            # Görüntüyü JPEG formatına kaydet
            image_stream = io.BytesIO()
            image.save(image_stream, format="JPEG")
            image_stream.seek(0)  # Stream'in başına dön
            print("Image successfully processed and converted to JPEG.")
        except UnidentifiedImageError:
            return JSONResponse(
                content={"error": "The uploaded file is not a valid image."},
                status_code=422  # Unprocessable Entity
            )
        except Exception as e:
            print(f"Error during image processing: {e}")
            return JSONResponse(
                content={"error": f"An error occurred during image processing: {str(e)}"},
                status_code=500  # Internal Server Error
            )

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
            return JSONResponse(
                content={"extracted_text": extracted_text},
                status_code=200  # OK
            )

        return JSONResponse(
            content={"error": "Text extraction failed"},
            status_code=400  # Bad Request
        )
    except Exception as e:
        # Hata durumunda hata mesajını döndürür
        print(f"Error Details: Endpoint={config.AZURE_ENDPOINT}, Key={config.AZURE_KEY}")
        print(f"Raw Error: {e}")
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500  # Internal Server Error
        )

    