from http.server import BaseHTTPRequestHandler
import json
import requests
import uuid

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        phone_input = data.get("number")
        
        # নম্বর ক্লিন করা
        target_num = phone_input.replace("+", "").replace(" ", "").replace("-", "").strip()
        if target_num.startswith("88"):
            target_num = target_num[2:]

        # SSLCommerz Sandbox Credentials
        STORE_ID = "testbox"
        STORE_PASS = "testbox@ssl"
        
        try:
            # সরাসরি SSLCommerz এ সেশন তৈরি করা
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
                'cus_name': 'ID_CHECK_NODE',
                'cus_email': 'verify@nexus.com',
                'cus_phone': target_num,
                'cus_add1': 'Dhaka',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'product_name': 'Identity_Verification',
                'product_category': 'OSINT',
                'product_profile': 'general'
            }

            response = requests.post(api_url, data=payload, timeout=10)
            res_data = response.json()

            if res_data.get('status') == 'SUCCESS':
                # সাকসেস হলে গেটওয়ে লিঙ্ক পাঠাবে
                final_result = {
                    "status": "success",
                    "gateway_url": res_data.get('GatewayPageURL')
                }
            else:
                final_result = {"status": "error", "message": "Gateway Rejected"}

        except Exception as e:
            final_result = {"status": "error", "message": "Connection Error"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(final_result).encode())
