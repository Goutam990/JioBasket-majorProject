import requests

from django.core.management.base import BaseCommand
from products.models import JioProduct

from products.product_list import jiomart as product_ids

class Command(BaseCommand):
    help = 'Update JioMart product data in the database'
    
    def fetch_product_data(self, product_id):
        api_url = f'https://www.jiomart.com/catalog/productdetails/get/{product_id}'
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Pin": "456001",
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'failure', 'message': response.statusText}

    def handle(self, *args, **options):
        for product_id in product_ids:
            data = self.fetch_product_data(product_id)

            if data.get('status') == 'success' and data.get('data'):
                product_info = data['data']
                
                JioProduct.objects.update_or_create(
                    id=product_id,
                    name = product_info.get('gtm_details', {}).get('name'),
                    price = product_info.get('selling_price'),
                    mrp = product_info.get('mrp'),
                    discount = product_info.get('discount'),
                    availability_status = product_info.get('availability_status'),
                    image_url = product_info.get('image_url'),
                )
            else:
                self.stderr.write(f"No product data found for ID: {product_id}. API response: {data}")