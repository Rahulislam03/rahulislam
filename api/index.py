from http.server import BaseHTTPRequestHandler
import json
import requests
import uuid

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            phone = data.get("number", "")

            # SSLCommerz সেশন তৈরি
            payload = {
                'store_id': 'testbox',
                'store_passwd': 'testbox@ssl',
                'total_amount': '10.00',
                'currency': 'BDT',
                'tran_id': str(uuid.uuid4())[:12],
                'success_url': 'https://google.com',
                'fail_url': 'https://google.com',
                'cancel_url': 'https://google.com',
                'cus_name': 'Identity_Check',
                'cus_email': 'verify@nexus.com',
                'cus_phone': phone,
                'cus_add1': 'Dhaka',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'product_name': 'Service',
                'product_category': 'OSINT',
                'product_profile': 'general'
            }

            r = requests.post("https://sandbox.sslcommerz.com/gwprocess/v4/api.php", data=payload, timeout=10)
            res = r.json()

            if res.get('status') == 'SUCCESS':
                response_data = {"status": "success", "url": res.get('GatewayPageURL')}
            else:
                response_data = {"status": "error", "message": "Gateway Busy"}

        except Exception as e:
            response_data = {"status": "error", "message": str(e)}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())
