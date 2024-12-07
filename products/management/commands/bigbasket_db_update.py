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
            "_bb_pin_code": "452010",
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
                    description = product_details.get("desc", None) + " " + product_details.get("w", "")
                    brand_name = product_details.get("brand", {}).get("name", None)
                    weight, unit = product_details.get("w", None).split()
                    category_llc = product_details.get("category", {}).get("llc_name", None)
                    pricing_info = product_details.get("pricing", {}).get("discount", {})
                    mrp = pricing_info.get("mrp", None)
                    selling_price = pricing_info.get("prim_price", {}).get("sp", None)
                    discount_text = pricing_info.get("d_text", None)
                    image_url = product_details.get("images")[0].get("m", None)
                    absolute_url = product_details.get("absolute_url", None)
                    availability_status = product_details.get("availability", {}).get("avail_status", None)
                    print(product_details.get("availability", {}))
                    if availability_status == "001":
                        availability_status = "A"
                    else:
                        availability_status = None

                    # Print the fetched details
                    print(f"Product ID: {product_id}")
                    print(f"Description: {description}")
                    print(f"Brand Name: {brand_name}")
                    print(f"Weight: {weight}")
                    print(f"Category LLC: {category_llc}")
                    print(f"MRP: {mrp}")
                    print(f"Selling Price: {selling_price}")
                    print(f"Discount Text: {discount_text}")
                    print(f"Availability Status: {availability_status}")
                    print("-" * 50)

                    return {
                        "name": description,
                        "brand": brand_name,
                        "quantity": weight,
                        "category": category_llc,
                        "mrp": mrp,
                        "price": selling_price,
                        "discount": discount_text,
                        "image_url": image_url,
                        "unit": unit,
                        "absolute_url": absolute_url,
                        "availability_status": availability_status
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
                    vendor="bigbasket",
                    brand=data["brand"],
                    defaults={
                        "category": data["category"],
                        "price":data["price"],
                        "mrp":data["mrp"],
                        "image_url":data["image_url"],
                        "quantity":data["quantity"],
                        "unit": data["unit"],
                        "absolute_url": "https://www.bigbasket.com" + data["absolute_url"],
                        "availability_status": data["availability_status"]
                    }
                )
            else:
                self.stderr.write(f"No product data found for ID: {product_id}. API response: {data}")