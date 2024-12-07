# Azure API bilgilerini tutuyoruz.
import os

if os.getenv("RENDER"):  # Render ortamında mı çalıştığını kontrol eder
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    AZURE_KEY = os.getenv("AZURE_KEY")
else:
    from dotenv import load_dotenv
    load_dotenv()  # Yerel geliştirme için .env dosyasını yükler
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    AZURE_KEY = os.getenv("AZURE_KEY")


