from http.server import BaseHTTPRequestHandler
import json
import requests
import uuid

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        phone_input = data.get("number", "")
        
        # নম্বর ক্লিন করা
        target_num = phone_input.replace("+", "").replace(" ", "").replace("-", "").strip()
        if target_num.startswith("88"):
            target_num = target_num[2:]

        # SSLCommerz স্যান্ডবক্স ক্রেডেনশিয়াল
        STORE_ID = "testbox"
        STORE_PASS = "testbox@ssl"
        
        try:
            api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
            payload = {
                'store_id': STORE_ID,
                'store_passwd': STORE_PASS,
                'total_amount': '10.00',
                'currency': 'BDT',
                'tran_id': str(uuid.uuid4())[:10],
                'success_url': 'https://google.com',
                'fail_url': 'https://google.com',
                'cancel_url': 'https://google.com',
                'cus_name': 'REAL_IDENTITY_CHECK',
                'cus_email': 'verify@nexus.com',
                'cus_phone': target_num,
                'cus_add1': 'Dhaka',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'product_name': 'ID_QUERY',
                'product_category': 'OSINT',
                'product_profile': 'general'
            }

            response = requests.post(api_url, data=payload, timeout=10)
            res_data = response.json()

            if res_data.get('status') == 'SUCCESS':
                final_output = {
                    "status": "success",
                    "url": res_data.get('GatewayPageURL')
                }
            else:
                final_output = {"status": "error", "message": "SSL_REJECTED"}

        except:
            final_output = {"status": "error", "message": "SERVER_TIMEOUT"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(final_output).encode())
