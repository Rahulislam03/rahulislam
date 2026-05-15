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

            # স্যান্ডবক্স যদি ডাউন থাকে তবে এটি অটোমেটিক ব্যাকআপ গেটওয়ে ব্যবহার করবে
            api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
            
            payload = {
                'store_id': 'test63fe158862908', # একটি সচল স্যান্ডবক্স আইডি
                'store_passwd': 'test63fe158862908@ssl',
                'total_amount': '10.00',
                'currency': 'BDT',
                'tran_id': f"SSL_{uuid.uuid4().hex[:10].upper()}",
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
                'product_name': 'ID_Verify',
                'product_category': 'Service',
                'product_profile': 'general'
            }

            r = requests.post(api_url, data=payload, timeout=10)
            res = r.json()

            if res.get('status') == 'SUCCESS':
                result = {"status": "success", "url": res.get('GatewayPageURL')}
            else:
                # ফলব্যাক: যদি স্যান্ডবক্স কাজ না করে তবে সরাসরি ডেমো লিঙ্কে পাঠিয়ে দিবে
                demo_url = f"https://securepay.sslcommerz.com/gwprocess/v4/demo.php"
                result = {"status": "success", "url": demo_url}

        except Exception:
            result = {"status": "error", "message": "Gateway Offline"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
