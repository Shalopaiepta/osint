import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")
TG_API_ID = os.getenv("TG_API_ID")
TG_API_HASH = os.getenv("TG_API_HASH")
TG_SESSION_NAME = os.getenv("TG_SESSION_NAME", "osint_session")

VK_API_VERSION = "5.131"
VK_API_BASE = "https://api.vk.com/method"

DDGS_MAX_RESULTS = 10


def validate_config():
    missing = [
        k for k, v in {
            "VK_TOKEN": VK_TOKEN,
            "TG_API_ID": TG_API_ID,
            "TG_API_HASH": TG_API_HASH,
        }.items() if not v
    ]
    if missing:
        raise EnvironmentError(f"Отсутствуют переменные окружения: {', '.join(missing)}")
