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

        # SSLCommerz Merchant Credentials
        # তুমি যদি রিয়েল মার্চেন্ট হও, তবে এখানে তোমার Store ID ও Password বসাবে।
        # আপাতত টেস্ট করার জন্য এগুলো স্যান্ডবক্স ক্রেডেনশিয়াল হিসেবে কাজ করবে।
        STORE_ID = "testbox" 
        STORE_PASS = "testbox@ssl"
        IS_SANDBOX = True # লাইভ হলে False করতে হবে

        base_url = "https://sandbox.sslcommerz.com" if IS_SANDBOX else "https://securepay.sslcommerz.com"

        payload = {
            'store_id': STORE_ID,
            'store_passwd': STORE_PASS,
            'total_amount': '10.00',
            'currency': 'BDT',
            'tran_id': str(uuid.uuid4())[:12], # ইউনিক ট্রানজেকশন আইডি
            'success_url': 'https://your-domain.com/success',
            'fail_url': 'https://your-domain.com/fail',
            'cancel_url': 'https://your-domain.com/cancel',
            'cus_name': 'Identity_Check',
            'cus_email': 'check@nexus.com',
            'cus_phone': phone_input,
            'cus_add1': 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_country': 'Bangladesh',
            'shipping_method': 'NO',
            'product_name': 'Digital_ID',
            'product_category': 'Verification',
            'product_profile': 'general'
        }

        try:
            # সরাসরি SSLCommerz গেটওয়েতে রিকোয়েস্ট পাঠানো হচ্ছে
            response = requests.post(f"{base_url}/gwprocess/v4/api.php", data=payload)
            res_data = response.json()

            if res_data.get('status') == 'SUCCESS':
                # এটি রিয়েল গেটওয়ে সেশন ডাটা রিটার্ন করবে
                final_response = {
                    "status": "success",
                    "data": {
                        "gateway_url": res_data.get('GatewayPageURL'),
                        "session_id": res_data.get('sessionkey'),
                        "system_status": "CONNECTED_TO_SSLCOMMERZ",
                        "verification_node": "MFS_ROUTING_ACTIVE"
                    }
                }
            else:
                final_response = {"status": "error", "message": "GATEWAY_REJECTED"}
        except Exception as e:
            final_response = {"status": "error", "message": str(e)}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(final_response).encode())
