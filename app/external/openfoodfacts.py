import requests
from typing import Optional, Dict
import time

class OpenFoodFactsClient:
    BASE_URL = "https://world.openfoodfacts.org/api/v0/product"

    def __init__(self, timeout: int = 8, max_retries: int = 2):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()

    def get_product(self, ean: str) -> Optional[Dict]:
        if not ean or len(ean) < 8:
            return None

        url = f"{self.BASE_URL}/{ean}.json"

        for attempt in range(self.max_retries + 1):
            try:
                resp = self.session.get(url, timeout=self.timeout)

                if resp.status_code == 404:
                    return None
                if resp.status_code != 200:
                    time.sleep(0.5 * (attempt + 1))
                    continue

                data = resp.json()
                if data.get("status") != 1:
                    return None

                product = data.get("product", {})
                return {
                    "ean": ean,
                    "name": product.get("product_name_it") or product.get("product_name") or "Nome sconosciuto",
                    "brand": product.get("brands") or "",
                    "ingredients_raw": product.get("ingredients_text_it") or product.get("ingredients_text") or "",
                    "image_url": product.get("image_url") or product.get("image_front_url"),
                    "source": "openfoodfacts"
                }
            except Exception:
                if attempt == self.max_retries:
                    return None
                time.sleep(1)
        return None