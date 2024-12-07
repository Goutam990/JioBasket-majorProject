import json, re
import requests

from django.core.management.base import BaseCommand
from products.models import Product

from products.product_list import jiomart as product_ids

class Command(BaseCommand):
    help = 'Update JioMart product data in the database'
    
    def fetch_product_data(self, product_id):
        api_url = f'https://www.jiomart.com/catalog/productdetails/get/{product_id}'
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Pin": "452010",
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'failure', 'message': response.statusText}

    def handle(self, *args, **options):
        for product_id in product_ids:
            data = self.fetch_product_data(product_id)
            # print(json.dumps(data, indent=4))

            if data.get('status') == 'success' and data.get('data'):
                base_url = "https://www.jiomart.com"
                
                product_info = data['data']
                
                name_tag = product_info['gtm_details']['name']
                name_tag = re.sub(r'[^a-zA-Z0-9]+', '-', name_tag).strip('-').lower()
                print(name_tag.lower())
                
                category = product_info["gtm_details"]['category'].lower()
                
                category = category[:category.index("/")]
                
                absolute_url = base_url + "/p/" +  category + "/" + name_tag + "/" + product_id
                
                
                Product.objects.update_or_create(
                    name = product_info.get('gtm_details', {}).get('name'),
                    vendor="jiomart",
                    defaults= {
                        "price" : product_info.get('selling_price'),
                        "mrp" : product_info.get('mrp'),
                        "discount" : product_info.get('discount'),
                        "availability_status" : product_info.get('availability_status'),
                        "image_url" : base_url + product_info["image_url"],
                        "brand" : product_info.get('gtm_details', {}).get('brand'),
                        "category" : product_info.get('gtm_details', {}).get('l4_category').split(",")[0],
                        "absolute_url" : absolute_url
                    }
                )
            else:
                self.stderr.write(f"No product data found for ID: {product_id}. API response: {data}")