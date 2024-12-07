# Azure API bilgilerini tutuyoruz.

from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# API bilgilerini al
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")

