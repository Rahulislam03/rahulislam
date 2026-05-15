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
            phone = data.get("number", "017XXXXXXXX")

            # SSLCommerz Sandbox Configuration
            api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
            
            # ট্রাই করার জন্য ৩টি ভিন্ন ভিন্ন ক্রেডেনশিয়ালস
            credentials = [
                {'id': 'test63fe158862908', 'pass': 'test63fe158862908@ssl'},
                {'id': 'testbox', 'pass': 'testbox@ssl'}
            ]

            final_url = "https://securepay.sslcommerz.com/gwprocess/v4/demo.php" # Fallback Demo
            success = False

            for cred in credentials:
                payload = {
                    'store_id': cred['id'],
                    'store_passwd': cred['pass'],
                    'total_amount': '10.00',
                    'currency': 'BDT',
                    'tran_id': f"SSL_{uuid.uuid4().hex[:8].upper()}",
                    'success_url': 'https://google.com',
                    'fail_url': 'https://google.com',
                    'cancel_url': 'https://google.com',
                    'cus_name': 'Tester',
                    'cus_email': 'test@test.com',
                    'cus_phone': phone,
                    'cus_add1': 'Dhaka',
                    'cus_city': 'Dhaka',
                    'cus_country': 'Bangladesh',
                    'shipping_method': 'NO',
                    'product_name': 'Verification',
                    'product_category': 'Service',
                    'product_profile': 'general'
                }

                r = requests.post(api_url, data=payload, timeout=10)
                if r.status_code == 200:
                    res = r.json()
                    if res.get('status') == 'SUCCESS':
                        final_url = res.get('GatewayPageURL')
                        success = True
                        break

            # স্যান্ডবক্স ডাউন থাকলেও অন্তত ডেমো গেটওয়ে ওপেন হবে
            result = {"status": "success", "url": final_url, "is_live": success}

        except Exception as e:
            result = {"status": "error", "message": "Gateway Offline"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
