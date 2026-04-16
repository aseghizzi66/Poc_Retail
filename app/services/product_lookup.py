from sqlalchemy.orm import Session
from redis import Redis
from typing import Optional, Dict
from app.external.openfoodfacts import OpenFoodFactsClient
from app.models import Product

class ProductLookupService:
    def __init__(self, db: Session, redis_client: Optional[Redis] = None):
        self.db = db
        self.redis = redis_client
        self.off_client = OpenFoodFactsClient()

    def get_or_fetch_product(self, ean: str, force_refresh: bool = False) -> Dict:
        cache_key = f"product:{ean}"

        # 1. Redis cache
        if self.redis and not force_refresh:
            cached = self.redis.get(cache_key)
            if cached:
                return cached

        # 2. DB locale
        product = self.db.query(Product).filter(Product.ean == ean).first()
        if product and not force_refresh:
            product_dict = {
                "ean": product.ean,
                "name": product.name,
                "brand": product.brand,
                "ingredients_raw": product.ingredients_raw,
                "image_url": product.image_url,
                "source": product.data_quality
            }
            if self.redis:
                self.redis.set(cache_key, product_dict, ex=86400)  # 24 ore
            return product_dict

        # 3. Open Food Facts
        off_data = self.off_client.get_product(ean)
        if off_data:
            # Salva nel DB
            new_product = Product(
                ean=off_data["ean"],
                name=off_data["name"],
                brand=off_data["brand"],
                ingredients_raw=off_data["ingredients_raw"],
                image_url=off_data.get("image_url"),
                data_quality="openfoodfacts"
            )
            self.db.add(new_product)
            self.db.commit()

            if self.redis:
                self.redis.set(cache_key, off_data, ex=86400)
            return off_data

        raise Exception(f"Prodotto {ean} non trovato né in DB né su Open Food Facts")