import json
import requests

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

from products.models import Product
from products.product_list import bigbasket as product_ids

class Command(BaseCommand):
    help = 'Update BigBasket product data in the database'

    def fetch_product_data(self, product_id):
    
        product_url = f"https://www.bigbasket.com/pd/{product_id}"
        
        cookies_dict = {
            "_bb_pin_code": "456001",
        }

        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

        response = requests.get(url=product_url, cookies=cookies_dict, headers=header)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})
            if data:
                try:
                    json_data = json.loads(data.string)
                    product_details = json_data["props"]["pageProps"]["productDetails"]["children"][0]

                    # Extract specific details using the paths provided
                    description = product_details.get("desc", "N/A")
                    brand_name = product_details.get("brand", {}).get("name", "N/A")
                    weight = product_details.get("w", "N/A")
                    category_llc = product_details.get("category", {}).get("llc_name", "N/A")
                    pricing_info = product_details.get("pricing", {}).get("discount", {})
                    mrp = pricing_info.get("mrp", "N/A")
                    selling_price = pricing_info.get("prim_price", {}).get("sp", "N/A")
                    discount_text = pricing_info.get("d_text", "N/A")

                    # Print the fetched details
                    print(f"Product ID: {product_id}")
                    print(f"Description: {description}")
                    print(f"Brand Name: {brand_name}")
                    print(f"Weight: {weight}")
                    print(f"Category LLC: {category_llc}")
                    print(f"MRP: {mrp}")
                    print(f"Selling Price: {selling_price}")
                    print(f"Discount Text: {discount_text}")
                    print("-" * 50)

                    return {
                        "name": description,
                        "brand": brand_name,
                        "weight": weight,
                        "category": category_llc,
                        "mrp": mrp,
                        "price": selling_price,
                        "discount": discount_text
                    }
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    return {}
            else:
                print("Script tag with ID = '__NEXT_DATA__' not found")
                return {}
        else:
            print(f"Failed to retrieve data for product ID {product_id}, status code: {response.status_code}")
            return {}

    def handle(self, *args, **options):
        for product_id in product_ids:
            data = self.fetch_product_data(product_id)
            print(json.dumps(data, indent=4))

            if len(data) != 0:
                
                Product.objects.update_or_create(
                    name=data["name"],
                    price=data["price"],
                    mrp=data["mrp"],
                    vendor="bigbasket",
                )
            else:
                self.stderr.write(f"No product data found for ID: {product_id}. API response: {data}")