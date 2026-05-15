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

            # SSLCommerz Sandbox API and Credentials
            # নিশ্চিত করো যে URL টি 'sandbox.sslcommerz.com'
            api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
            
            payload = {
                'store_id': 'testbox', # স্যান্ডবক্সের জন্য এটাই ডিফল্ট
                'store_passwd': 'testbox@ssl',
                'total_amount': '10.00',
                'currency': 'BDT',
                'tran_id': f"REF_{uuid.uuid4().hex[:10].upper()}",
                'success_url': 'https://google.com',
                'fail_url': 'https://google.com',
                'cancel_url': 'https://google.com',
                'cus_name': 'Rahul_Islam',
                'cus_email': 'rahul@mixveo.com',
                'cus_phone': phone,
                'cus_add1': 'Dhaka',
                'cus_city': 'Dhaka',
                'cus_country': 'Bangladesh',
                'shipping_method': 'NO',
                'product_name': 'Service_Verify',
                'product_category': 'Verification',
                'product_profile': 'general'
            }

            # Form-encoded data পাঠানো জরুরি
            response = requests.post(api_url, data=payload, timeout=15)
            
            # রেসপন্স চেক করা
            if response.status_code == 200:
                try:
                    res_json = response.json()
                    if res_json.get('status') == 'SUCCESS':
                        result = {"status": "success", "url": res_json.get('GatewayPageURL')}
                    else:
                        # সার্ভার থেকে আসা আসল এরর মেসেজটি দেখাবে
                        reason = res_json.get('failedreason', 'Merchant account is not active in Sandbox')
                        result = {"status": "error", "message": reason}
                except:
                    result = {"status": "error", "message": "Invalid response from SSLCommerz"}
            else:
                result = {"status": "error", "message": f"Server connection failed ({response.status_code})"}

        except Exception as e:
            result = {"status": "error", "message": "Request timed out. Try again."}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
