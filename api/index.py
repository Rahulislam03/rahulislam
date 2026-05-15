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

            # SSLCommerz Sandbox API
            api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
            
            # বিকল্প স্যান্ডবক্স ক্রেডেনশিয়ালস (যদি testbox কাজ না করে)
            payload = {
                'store_id': 'test63fe158862908', 
                'store_passwd': 'test63fe158862908@ssl',
                'total_amount': '10.00',
                'currency': 'BDT',
                'tran_id': f"SSL_{uuid.uuid4().hex[:10].upper()}",
                'success_url': 'https://google.com',
                'fail_url': 'https://google.com',
                'cancel_url': 'https://google.com',
                'cus_name': 'Islam Rahul',
                'cus_email': 'rahul@mixveo.com',
                'cus_phone': phone,
                'cus_add1': 'Dhaka',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'product_name': 'ID_Verify',
                'product_category': 'Service',
                'product_profile': 'general'
            }

            # API Call
            response = requests.post(api_url, data=payload, timeout=15)
            
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get('status') == 'SUCCESS':
                    result = {"status": "success", "url": res_json.get('GatewayPageURL')}
                else:
                    # আসল এরর মেসেজটি ধরবে
                    error_msg = res_json.get('failedreason', 'Gateway Busy')
                    result = {"status": "error", "message": error_msg}
            else:
                result = {"status": "error", "message": "Server Connection Failed"}

        except Exception as e:
            result = {"status": "error", "message": "Connection Timeout"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
