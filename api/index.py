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
            phone = data.get("number", "01700000000")

            # SSLCommerz Sandbox Credentials
            api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
            payload = {
                'store_id': 'testbox',
                'store_passwd': 'testbox@ssl',
                'total_amount': '10.00',
                'currency': 'BDT',
                'tran_id': f"TRANS_{uuid.uuid4().hex[:8].upper()}",
                'success_url': 'https://www.google.com',
                'fail_url': 'https://www.google.com',
                'cancel_url': 'https://www.google.com',
                'cus_name': 'ID_CHECKER',
                'cus_email': 'verify@nexus.com',
                'cus_phone': phone,
                'cus_add1': 'Dhaka',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'product_name': 'Identity_Node',
                'product_category': 'OSINT',
                'product_profile': 'general'
            }

            # API Call with proper headers
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            r = requests.post(api_url, data=payload, headers=headers, timeout=15)
            
            # ট্রাবলশুটিং এর জন্য চেক
            if r.status_code == 200:
                res_data = r.json()
                if res_data.get('status') == 'SUCCESS':
                    response_final = {"status": "success", "url": res_data.get('GatewayPageURL')}
                else:
                    response_final = {"status": "error", "message": res_data.get('failedreason', 'Gateway Rejected')}
            else:
                response_final = {"status": "error", "message": f"Server Error: {r.status_code}"}

        except Exception as e:
            response_final = {"status": "error", "message": "Connection Timeout. Try Again."}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_final).encode())
